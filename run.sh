#!/usr/bin/env bash
# Baldic Dream2Distro - Linux baslatici
cd "$(dirname "$0")" || exit 1
command -v python3 >/dev/null || { echo "python3 bulunamadi."; exit 1; }
python3 -c "import PySide6" 2>/dev/null || {
  echo "Gerekli paketler kuruluyor..."
  python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null \
    || python3 -m pip install -r requirements.txt || {
      echo "Kurulamadi. Deneyin: sudo apt install python3-pyside6.qtquick python3-pil"
      exit 1; }
}
exec python3 main.py
