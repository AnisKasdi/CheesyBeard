import pymem
import pymem.pattern
import re

class MemoryManager:
    def __init__(self, process_name="Transformice.exe"):
        self.process_name = process_name
        self.pm = None
        self.connected = False

    def connect(self):
        try:
            self.pm = pymem.Pymem(self.process_name)
            self.connected = True
            return True
        except Exception as e:
            self.connected = False
            return False

    def pattern_to_regex(self, pattern):
        """Converts an AOB pattern (e.g., 'AA ?? BB') to a regex byte pattern."""
        # Remove spaces
        pattern = pattern.replace(' ', '')
        # Convert ?? to . (dot matches any char in regex, but we need bytes)
        # Actually pymem's pattern_scan_all takes a bytes pattern where wildcards are handled differently
        # or we can use regex on the memory dump.
        # But pymem has a built-in pattern scanner.
        # Pymem's pattern_scan_all accepts a regex string if we construct it right.
        
        # Let's use the standard approach:
        # Convert "AA ?? BB" to b'\xAA.\xBB' regex style
        regex_pattern = b''
        for i in range(0, len(pattern), 2):
            byte_str = pattern[i:i+2]
            if byte_str == '??':
                regex_pattern += b'.'
            else:
                regex_pattern += re.escape(bytes.fromhex(byte_str))
        return regex_pattern

    def scan_aob(self, aob_pattern):
        if not self.connected:
            return None
        
        try:
            regex = self.pattern_to_regex(aob_pattern)
            print(f"Scanning for pattern: {aob_pattern}")
            
            # 1. Try scanning main module first (fastest)
            try:
                modules = list(self.pm.list_modules())
                for module in modules:
                    res = pymem.pattern.pattern_scan_module(self.pm.process_handle, module, regex)
                    if res:
                        print(f"Found in module {module.name} at {hex(res)}")
                        return res
            except:
                pass

            # 2. Custom Region Scan (slower but thorough)
            # This mimics Cheat Engine's scan with "Writable" unchecked (scans everything readable)
            address = 0
            while address < 0x7FFFFFFF: # User mode limit approx
                try:
                    mbi = pymem.memory.virtual_query(self.pm.process_handle, address)
                    if not mbi:
                        address += 4096 # Skip if query fails
                        continue
                    
                    # Check if memory is committed and readable
                    # MEM_COMMIT = 0x1000
                    # PAGE_NOACCESS = 0x01, PAGE_GUARD = 0x100
                    if mbi.State == 0x1000 and not (mbi.Protect & 0x100) and not (mbi.Protect & 0x01):
                        # Read the chunk
                        try:
                            chunk = self.pm.read_bytes(address, mbi.RegionSize)
                            # Search regex in chunk
                            match = re.search(regex, chunk, re.DOTALL)
                            if match:
                                found_addr = address + match.start()
                                print(f"Found in region {hex(address)} at {hex(found_addr)}")
                                return found_addr
                        except:
                            pass # Failed to read this chunk
                    
                    address += mbi.RegionSize
                except Exception as e:
                    # print(f"Region scan error: {e}")
                    address += 4096
            
            print("Pattern not found in any region.")
            return None
            
        except Exception as e:
            print(f"Scan error: {e}")
            return None

    def write_bytes(self, address, byte_string):
        """Writes a string of bytes (e.g. '90 90') to address."""
        if not self.connected or not address:
            return False
        
        try:
            bytes_to_write = bytes.fromhex(byte_string.replace(' ', ''))
            self.pm.write_bytes(address, bytes_to_write, len(bytes_to_write))
            return True
        except Exception as e:
            print(f"Write error: {e}")
            return False

    def read_bytes(self, address, length):
        if not self.connected or not address:
            return None
        try:
            return self.pm.read_bytes(address, length)
        except:
            return None

class Cheat:
    def __init__(self, name, scan_pattern, replace_pattern, memory_manager):
        self.name = name
        self.scan_pattern = scan_pattern
        self.replace_pattern = replace_pattern
        self.mm = memory_manager
        self.address = None
        self.original_bytes = None
        self.active = False

    def toggle(self):
        if not self.mm.connected:
            return "Not connected to game."

        if self.active:
            return self.deactivate()
        else:
            return self.activate()

    def activate(self):
        if self.active:
            return "Already active."

        # 1. Find address if not known
        if self.address is None:
            self.address = self.mm.scan_aob(self.scan_pattern)
            if self.address is None:
                return f"Could not find AOB for {self.name}"

        # 2. Prepare replacement bytes
        # We need to handle '??' in the replacement pattern
        replace_parts = self.replace_pattern.split(' ')
        replace_len = len(replace_parts)
        
        current_bytes = self.mm.read_bytes(self.address, replace_len)
        if not current_bytes:
            return "Failed to read memory."
            
        self.original_bytes = current_bytes
        
        # Construct the actual bytes to write
        bytes_to_write = bytearray()
        for i, part in enumerate(replace_parts):
            if part == '??':
                # Keep original byte
                bytes_to_write.append(current_bytes[i])
            else:
                try:
                    bytes_to_write.append(int(part, 16))
                except ValueError:
                    return f"Invalid replacement byte: {part}"

        # 3. Write replacement
        # We use pymem directly here since we have a bytearray
        try:
            self.mm.pm.write_bytes(self.address, bytes(bytes_to_write), len(bytes_to_write))
            self.active = True
            return f"{self.name} Activated!"
        except Exception as e:
            return f"Failed to write memory: {e}"

    def deactivate(self):
        if not self.active:
            return "Not active."

        if self.address and self.original_bytes:
            # Convert bytes object back to hex string for our write_bytes method
            # Or just use pm.write_bytes directly. 
            # Let's use mm.write_bytes but we need to format it.
            # Actually, let's add a raw write method or just format it.
            original_hex = self.original_bytes.hex()
            if self.mm.write_bytes(self.address, original_hex):
                self.active = False
                return f"{self.name} Deactivated."
            else:
                return "Failed to restore memory."
        return "Error: No address or backup."
