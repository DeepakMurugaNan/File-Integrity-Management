@echo off
echo Starting Launcher...
cd /d "%~dp0"
call "..\fim-env\Scripts\activate.bat"
start pythonw FIM_Launcher.py
exit
