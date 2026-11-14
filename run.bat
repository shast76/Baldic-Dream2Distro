@echo off
REM Baldic Dream2Distro - Windows baslatici
cd /d "%~dp0"
where python >nul 2>&1 || (
  echo Python bulunamadi. https://python.org adresinden kurun.
  echo Kurarken "Add Python to PATH" secenegini isaretleyin.
  pause & exit /b 1
)
python -c "import PySide6" >nul 2>&1 || (
  echo Gerekli paketler kuruluyor...
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt || (pause & exit /b 1)
)
python main.py
if errorlevel 1 pause
