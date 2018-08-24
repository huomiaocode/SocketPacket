:定位到当前的目录
cd %~dp0

python "C:\pyinstaller-3.3.1\pyinstaller.py" --onefile --icon=assets/icon.ico --windowed SocketPacket.py

pause