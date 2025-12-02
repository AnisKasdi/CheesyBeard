# CheesyBeard - Transformice Educational Tool

**Author:** Anis K. (Student in Computer Science)
**Version:** 1.0

> [!WARNING]
> **DISCLAIMER**: This software is for **EDUCATIONAL PURPOSES ONLY**. The author is not responsible for any misuse of this tool. Using cheats in online games violates Terms of Service and can lead to account bans. Use at your own risk.

---

## 🐭 User Guide

### How to Install
1.  Download the installer `CheesyBeard_Setup.exe`.
2.  Run the installer and follow the instructions (Next > Next > Finish).
3.  A shortcut **CheesyBeard** will be created on your desktop.

### How to Use
1.  **Start the Game**: Open *Transformice* (Standalone version recommended).
2.  **Open CheesyBeard**: Double-click the icon on your desktop.
3.  **Connect**: The tool will automatically search for the game.
    -   **Status Orange**: Searching for game...
    -   **Status Green**: Connected!
4.  **Cheat**: Toggle the switches to activate or deactivate features.

---

## 👨‍💻 Developer Guide

This section explains how the tool was built for educational purposes.

### Technical Breakdown

#### 1. Memory Analysis
We used **Cheat Engine** to analyze the game's memory structure.
-   **AOB Scanning**: Instead of static addresses, we use **Array of Bytes (AOB)** signatures to find code locations even after game updates.
-   **Wildcards**: We use wildcards (`??`) in our patterns to handle dynamic memory addresses.

#### 2. Python Implementation
The tool is built with Python using:
-   `pymem`: For reading/writing process memory.
-   `customtkinter`: For the modern dark-mode GUI.
-   `ctypes`: For Windows API integration (Taskbar icons, etc.).

#### 3. Custom Memory Scanner
Standard memory scanners often skip "Read-Only" executable memory where the game code lives. We implemented a custom scanner using `virtual_query` to iterate through all committed memory regions, ensuring we find the code patterns.

### How to Build from Source

If you want to modify the code and build your own executable:

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Build**:
    Run the `build.bat` script. This will use **PyInstaller** to generate:
    -   `dist/CheesyBeard.exe` (Portable)
    -   `dist/CheesyBeard_Setup.exe` (Installer)

### Credits
Created by **Anis K.** as a project to demonstrate low-level memory manipulation and GUI development in Python.
