import sys
import os
from pathlib import Path

if sys.platform == "win32":
    import ctypes
    
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.FreeConsole()
    
    try:
        myappid = 'ryderdev.repoprep.1.0.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from ui.main_window import MainWindow

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    
    app.setApplicationName("RepoPrep")
    app.setOrganizationName("RyderDev")
    app.setApplicationDisplayName("RepoPrep Pro")
    app.setApplicationVersion("1.0.0")
    
    icon_path = Path(__file__).parent / "icon.ico"
    if icon_path.exists():
        app_icon = QIcon(str(icon_path))
        app.setWindowIcon(app_icon)
        
        QApplication.setWindowIcon(app_icon)
    else:
        print("Icon file not found, using default icon")
    
    window = MainWindow()
    
    if sys.platform == "win32":
        window.setWindowFlags(
            window.windowFlags() | 
            Qt.WindowSystemMenuHint | 
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint |
            Qt.WindowCloseButtonHint
        )
        
        window.setWindowTitle("RepoPrep v1.0.0")
        if icon_path.exists():
            window.setWindowIcon(app_icon)
    
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()