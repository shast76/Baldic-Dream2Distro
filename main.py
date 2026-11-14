#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baldic Dream2Distro
===================
Kendi Linux dagitiminizi yapan arac.

Calistirmak icin:
    pip install PySide6 Pillow
    python main.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

def _app_dir() -> Path:
    """Paketlenmis .exe icinde dosyalar gecici klasorde durur."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", None)
        return Path(base) if base else Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_DIR = _app_dir()
sys.path.insert(0, str(APP_DIR))


def run_netboot_service() -> int:
    """Paketlenmis .exe icinde servis kipi.

    PyInstaller ile derlendiginde sys.executable Python degil uygulamanin
    kendisidir; servisi ayri surec olarak baslatirken bu bayrakla kendimizi
    cagiriyoruz."""
    from d2d.netboot.runner import main as runner_main
    args = [a for a in sys.argv[1:] if a != "--netboot-service"]
    return runner_main(args)


def main() -> int:
    try:
        from PySide6.QtCore import QCoreApplication, Qt, QUrl
        from PySide6.QtGui import QGuiApplication, QIcon
        from PySide6.QtQml import QQmlApplicationEngine
        from PySide6.QtQuick import QQuickWindow
    except ImportError:
        sys.stderr.write(
            "\nPySide6 kurulu degil.\n\n"
            "Kurmak icin:\n"
            "    pip install PySide6 Pillow\n\n"
            "Not: Linux'ta ayrica 'python3-pyside6.qtquick' paketi de kullanilabilir.\n")
        return 1

    from d2d.bridge import Bridge
    from d2d.grub_bridge import GrubBridge
    from d2d.netboot.bridge import NetbootBridge

    QCoreApplication.setApplicationName("Baldic Dream2Distro")
    QCoreApplication.setOrganizationName("Baldic")

    # Windows'ta yazilim isleme daha az sorun cikariyor
    if os.name == "nt" and not os.environ.get("QSG_RHI_BACKEND"):
        os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

    app = QGuiApplication(sys.argv)
    icon_path = APP_DIR / "assets" / "icon.png"
    if icon_path.is_file():
        app.setWindowIcon(QIcon(str(icon_path)))

    bridge = Bridge()
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("app", bridge)
    grub_bridge = GrubBridge()
    ctx.setContextProperty("grub", grub_bridge)
    netboot_bridge = NetbootBridge()
    ctx.setContextProperty("netboot", netboot_bridge)
    ctx.setContextProperty("assetsDir",
                           QUrl.fromLocalFile(str(APP_DIR / "assets")).toString())

    engine.addImportPath(str(APP_DIR / "qml"))
    engine.load(QUrl.fromLocalFile(str(APP_DIR / "qml" / "Main.qml")))
    if not engine.rootObjects():
        sys.stderr.write("Arayuz yuklenemedi. qml klasoru eksik olabilir.\n")
        return 1

    app.aboutToQuit.connect(bridge.shutdown)
    app.aboutToQuit.connect(netboot_bridge.shutdown)
    # motoru arka planda baslatmayi dene
    from PySide6.QtCore import QTimer
    QTimer.singleShot(400, bridge.startEngine)
    return app.exec()


if __name__ == "__main__":
    if "--netboot-service" in sys.argv:
        sys.exit(run_netboot_service())
    sys.exit(main())
