from memory_manager import MemoryManager, Cheat
from gui import CheatApp

def main():
    # Initialize Memory Manager
    mm = MemoryManager("Transformice.exe")

    # Define Cheats
    # Note: '??' in replacement means keep original byte
    cheats_data = [
        {
            "name": "Undead Mouse",
            "scan": "F2 0F 2A ?? 66 0F 2E C1 0F 97 ?? 0F b6 ?? 89 ?? ?? 8B ?? ?? 85 ?? 0F 84 ?? 01 00 00",
            "replace": "F2 0F 40"
        },
        {
            "name": "Rato Agil Forte",
            "scan": "F3 0F 7E ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? F3 0F 7E 8E ?? ?? ?? ?? F2 0F 5E ??",
            "replace": "F2 0F 5E 85"
        },
        {
            "name": "Spawn Shaman Items",
            "scan": "8B ?? ?? 89 ?? ?? 85 ?? 74 17 8B ?? ?? FB ff ff 85 ?? 0F 84 ?? ?? ?? ?? 8B ?? ?? ?? 00 00 89 ?? ?? 8B ?? ?? 85 ?? 0F 84 ?? ?? 00 00 8B ?? 8D ?? ?? ?? 00 00 8D ?? ?? FB FF FF",
            "replace": "8D"
        },
        {
            "name": "Anti-Cannon",
            "scan": "F2 0F 5E C1 66 0F D6 86 ?? 00 00 00 8B ?? ?? ?? ?? ?? ??",
            "replace": "F2 0F 10"
        },
        {
            "name": "Speed Wind Shaman",
            "scan": "F2 0F 59 C1 66 0F D6 40 ?? 8D ?? ?? ?? 00 00 8D ??",
            "replace": "F2 0F 2A"
        },
        {
            "name": "Matrix Hack",
            "scan": "F3 0F 6F 06 66 0F 6F 0F F3 0F 70 D0 FF F2 0F 70 D2 FF 66 0F 6F DC 66 0F D9 DA 66 0F D5 D9 66 0F 71 D3 08 66 0F FD D8 66 0F 7F 1F 83 C6 10 83 C7 10",
            "replace": "?? ?? 10"
        },
        {
            "name": "Auto-Win (Fixed)",
            "scan": "F2 0f 2a C8 F2 0F 59 C9 F2 0F 58",
            "replace": "F2 0f 00 C8 F2 0F 59 C9 F2 0F 10"
        },
        {
            "name": "Fly Hack (Ground)",
            "scan": "F3 0F 7E ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? F3 0F 7E ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 8D 8F",
            "replace": "F3 0F 10"
        },
        {
            "name": "Elevator Hack",
            "scan": "F2 0F 59 CB F2 0F 59 C2 F2 0F 58 C8 66 0F D6 8D",
            "replace": "F2 0F 40"
        }
    ]

    cheats = []
    for data in cheats_data:
        cheats.append(Cheat(data["name"], data["scan"], data["replace"], mm))

    # Start GUI
    app = CheatApp(mm, cheats)
    app.mainloop()

if __name__ == "__main__":
    main()
