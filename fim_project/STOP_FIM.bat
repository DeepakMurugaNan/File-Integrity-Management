@echo off
echo Stopping FIM processes...
echo.
echo Closing FIM Dashboard...
taskkill /FI "WINDOWTITLE eq FIM Dashboard*" /T /F
echo.
echo Closing FIM Watcher...
taskkill /FI "WINDOWTITLE eq FIM Watcher*" /T /F
echo.
echo Closing FIM Scanner...
taskkill /FI "WINDOWTITLE eq FIM Scanner*" /T /F
echo.
echo Closing hidden Python processes (if any)...
taskkill /IM python.exe /F 2>nul
echo.
echo All FIM processes stopped.
pause
