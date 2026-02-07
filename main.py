import sys
import os
from pathlib import Path

# Hide console window on Windows
if sys.platform == "win32":
    import ctypes
    from ctypes import windll
    
    try:
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
            ctypes.windll.kernel32.FreeConsole()
    except Exception:
        pass
    
    # Set AppUserModelID for taskbar icon display (MUST be before QApplication)
    try:
        myappid = 'ryderdev.repoprep.1.1.0'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        print(f"Warning: Could not set AppUserModelID: {e}")

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up error handling
import traceback
import logging

# Configure logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=str(log_dir / "repoprep.log"),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QIcon

    from ui.main_window import MainWindow

    def main():
        """Main application entry point"""
        try:
            # Enable high DPI scaling
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
            
            # Create application
            app = QApplication(sys.argv)
            
            # Set application metadata
            app.setApplicationName("RepoPrep")
            app.setOrganizationName("RyderDev")
            app.setApplicationDisplayName("RepoPrep - Project Cleaner")
            app.setApplicationVersion("1.1.0")
            
            # Set application icon from multiple possible locations
            possible_paths = [
                Path(sys._MEIPASS) / "icon.ico" if hasattr(sys, '_MEIPASS') else None,
                Path(__file__).parent / "icon.ico",
                Path.cwd() / "icon.ico",
            ]
            
            app_icon = None
            for path in possible_paths:
                if path and path.exists():
                    try:
                        app_icon = QIcon(str(path))
                        break
                    except Exception:
                        continue
            
            if app_icon and not app_icon.isNull():
                app.setWindowIcon(app_icon)
                QApplication.setWindowIcon(app_icon)
            
            # Create and configure main window
            window = MainWindow()
            
            # Apply Windows-specific settings
            if sys.platform == "win32":
                try:
                    window.setWindowFlags(
                        window.windowFlags() | 
                        Qt.WindowSystemMenuHint | 
                        Qt.WindowMinimizeButtonHint |
                        Qt.WindowMaximizeButtonHint |
                        Qt.WindowCloseButtonHint
                    )
                    
                    window.setWindowTitle("RepoPrep v1.1.0")
                    if app_icon and not app_icon.isNull():
                        window.setWindowIcon(app_icon)
                except Exception as e:
                    print(f"Warning: Could not apply Windows settings: {e}")
            
            # Show window and run application
            window.show()
            
            sys.exit(app.exec())
        
        except Exception as e:
            error_msg = f"Application Error: {str(e)}\n\n{traceback.format_exc()}"
            logging.error(error_msg)
            print(error_msg)
            sys.exit(1)

    if __name__ == "__main__":
        main()

except ImportError as e:
    error_msg = f"Missing required module: {str(e)}\n\nPlease install requirements:\npip install -r requirements.txt"
    print(error_msg)
    logging.error(error_msg)
    sys.exit(1)

except Exception as e:
    error_msg = f"Fatal Error: {str(e)}\n\n{traceback.format_exc()}"
    print(error_msg)
    logging.error(error_msg)
    sys.exit(1)