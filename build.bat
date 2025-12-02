@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Building CheesyBeard App...
pyinstaller --noconfirm --onefile --windowed --icon "src/pirate_icone.ico" --add-data "src;src" --name "CheesyBeard" main.py

echo Building Installer...
pyinstaller --noconfirm --onefile --windowed --icon "src/pirate_icone.ico" --name "CheesyBeard_Setup" create_installer.py

echo Build complete! Check the 'dist' folder for CheesyBeard_Setup.exe
pause
