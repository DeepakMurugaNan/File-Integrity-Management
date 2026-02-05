echo Starting Real-Time FIM Watcher...
title FIM Watcher
echo Press Ctrl+C to stop.
cd /d "%~dp0"
"..\fim-env\Scripts\python.exe" manage.py watch_fim
pause
