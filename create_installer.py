import customtkinter as ctk
import os
import shutil
import shutil
import sys
from win32com.client import Dispatch

class InstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CheesyBeard Setup")
        self.geometry("500x400")
        ctk.set_appearance_mode("Dark")
        
        self.install_dir = os.path.join(os.environ['LOCALAPPDATA'], "CheesyBeard")
        
        # Pages
        self.frames = {}
        self.current_frame = None
        
        self.setup_pages()
        self.show_frame("Welcome")

    def setup_pages(self):
        # Welcome Page
        welcome_frame = ctk.CTkFrame(self)
        ctk.CTkLabel(welcome_frame, text="Welcome to CheesyBeard Setup", font=("Roboto", 20, "bold")).pack(pady=40)
        ctk.CTkLabel(welcome_frame, text="This wizard will install CheesyBeard on your computer.\n\nClick Next to continue.", font=("Roboto", 14)).pack(pady=20)
        ctk.CTkButton(welcome_frame, text="Next >", command=lambda: self.show_frame("Location")).pack(side="bottom", pady=40)
        self.frames["Welcome"] = welcome_frame

        # Location Page
        loc_frame = ctk.CTkFrame(self)
        ctk.CTkLabel(loc_frame, text="Select Installation Folder", font=("Roboto", 20, "bold")).pack(pady=20)
        
        self.dir_entry = ctk.CTkEntry(loc_frame, width=300)
        self.dir_entry.insert(0, self.install_dir)
        self.dir_entry.pack(pady=10)
        
        ctk.CTkLabel(loc_frame, text="The software will be installed in the folder above.", font=("Roboto", 12)).pack(pady=10)
        
        nav_frame = ctk.CTkFrame(loc_frame, fg_color="transparent")
        nav_frame.pack(side="bottom", pady=40)
        ctk.CTkButton(nav_frame, text="< Back", command=lambda: self.show_frame("Welcome")).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Install", command=self.install).pack(side="left", padx=10)
        self.frames["Location"] = loc_frame

        # Finish Page
        finish_frame = ctk.CTkFrame(self)
        self.finish_label = ctk.CTkLabel(finish_frame, text="Installing...", font=("Roboto", 20, "bold"))
        self.finish_label.pack(pady=40)
        self.finish_status = ctk.CTkLabel(finish_frame, text="Please wait...", font=("Roboto", 14))
        self.finish_status.pack(pady=20)
        self.close_btn = ctk.CTkButton(finish_frame, text="Finish", command=self.destroy, state="disabled")
        self.close_btn.pack(side="bottom", pady=40)
        self.frames["Finish"] = finish_frame

    def show_frame(self, name):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = self.frames[name]
        self.current_frame.pack(fill="both", expand=True)

    def install(self):
        self.show_frame("Finish")
        self.update()
        
        target_dir = self.dir_entry.get()
        
        try:
            # 1. Create Directory
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # 2. Copy Files
            # We assume 'dist/CheesyBeard.exe' exists relative to this script
            exe_source = os.path.join("dist", "CheesyBeard.exe")
            if not os.path.exists(exe_source):
                self.finish_status.configure(text="Error: CheesyBeard.exe not found in dist folder.\nPlease build it first.")
                return

            shutil.copy2(exe_source, target_dir)
            
            # 3. Create Shortcut
            self.create_shortcut(os.path.join(target_dir, "CheesyBeard.exe"))
            
            self.finish_label.configure(text="Installation Complete!")
            self.finish_status.configure(text=f"CheesyBeard has been installed to:\n{target_dir}")
            self.close_btn.configure(state="normal")
            
        except Exception as e:
            self.finish_label.configure(text="Installation Failed")
            self.finish_status.configure(text=str(e))

    def create_shortcut(self, target_path):
        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        path = os.path.join(desktop, "CheesyBeard.lnk")
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.IconLocation = target_path
        shortcut.save()

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
