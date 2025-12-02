import customtkinter as ctk
import threading
import time
from PIL import Image, ImageTk
import os
import ctypes

class CheatApp(ctk.CTk):
    def __init__(self, memory_manager, cheats):
        super().__init__()

        # Set AppUserModelID for taskbar icon
        myappid = 'cheesybeard.cheat.tool.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.mm = memory_manager
        self.cheats = cheats

        self.title("CheesyBeard - TFM Hack")
        self.geometry("400x700")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Set Icon
        try:
            # Icons are in 'src' folder
            icon_path = os.path.join(os.path.dirname(__file__), "src", "pirate_icone.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
            else:
                print(f"Icon not found at {icon_path}")
        except Exception as e:
            print(f"Failed to load icon: {e}")

        # Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(pady=20, padx=20, fill="x")

        # Fun Image
        try:
            fun_img_path = os.path.join(os.path.dirname(__file__), "src", "icone_fun.png")
            if os.path.exists(fun_img_path):
                fun_img = Image.open(fun_img_path)
                fun_img = fun_img.resize((100, 100), Image.Resampling.LANCZOS)
                fun_photo = ctk.CTkImage(light_image=fun_img, dark_image=fun_img, size=(100, 100))
                
                self.image_label = ctk.CTkLabel(self.header_frame, image=fun_photo, text="")
                self.image_label.pack(pady=5)
        except Exception as e:
            print(f"Failed to load fun image: {e}")

        self.label_title = ctk.CTkLabel(self.header_frame, text="CheesyBeard", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=5)

        self.status_label = ctk.CTkLabel(self.header_frame, text="Status: Connecting...", text_color="orange")
        self.status_label.pack(pady=5)

        # Cheats List
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Available Cheats")
        self.scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.switches = []
        for cheat in self.cheats:
            switch = ctk.CTkSwitch(
                self.scrollable_frame, 
                text=cheat.name, 
                command=lambda c=cheat: self.toggle_cheat(c)
            )
            switch.pack(pady=10, padx=10, anchor="w")
            self.switches.append(switch)

        # Log Area
        self.log_textbox = ctk.CTkTextbox(self, height=100)
        self.log_textbox.pack(pady=20, padx=20, fill="x")
        self.log_textbox.insert("0.0", "Welcome to CheesyBeard.\n")

        # Start connection thread
        self.running = True
        self.connect_thread = threading.Thread(target=self.monitor_connection)
        self.connect_thread.daemon = True # Daemon thread dies with main app
        self.connect_thread.start()

    def log(self, message):
        # Schedule log update on main thread
        self.after(0, lambda: self._log_internal(message))

    def _log_internal(self, message):
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")

    def update_status(self, text, color):
        # Schedule status update on main thread
        self.after(0, lambda: self.status_label.configure(text=text, text_color=color))

    def toggle_cheat(self, cheat):
        result = cheat.toggle()
        self.log(f"[{cheat.name}]: {result}")

    def monitor_connection(self):
        while self.running:
            if not self.mm.connected:
                if self.mm.connect():
                    self.update_status("Status: Connected", "green")
                    self.log("Connected to Transformice!")
                else:
                    self.update_status("Status: Searching for game...", "orange")
            else:
                try:
                    if not self.mm.pm.process_handle:
                        self.mm.connected = False
                except:
                    self.mm.connected = False
            
            time.sleep(2)

    def on_closing(self):
        self.running = False
        self.destroy()
