@echo off
echo Creating Admin User...
cd /d "%~dp0"
call "..\fim-env\Scripts\activate.bat"
winpty python manage.py createsuperuser
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 'winpty' not found, trying standard python...
    python manage.py createsuperuser
)
pause
