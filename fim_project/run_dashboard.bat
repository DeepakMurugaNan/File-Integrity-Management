@echo off
title FIM Dashboard
echo Starting FIM Dashboard...
cd /d "%~dp0"
"..\fim-env\Scripts\python.exe" manage.py runserver
pause
