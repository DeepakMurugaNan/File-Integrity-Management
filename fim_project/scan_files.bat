echo Starting FIM Scan...
title FIM Scanner
cd /d "%~dp0"
"..\fim-env\Scripts\python.exe" manage.py run_fim
pause
