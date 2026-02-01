import os
import shutil
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QTextEdit, QGroupBox, QFileDialog,
    QMessageBox, QStatusBar, QProgressBar, QMenuBar, QMenu, QGridLayout
)
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QFont, QIcon

from .styles import STYLESHEET

class CleaningThread(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(bool)
    progress_signal = Signal(int)
    
    def __init__(self, source_dir: str, target_dir: str):
        super().__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir
    
    def run(self):
        try:
            source = Path(self.source_dir)
            target = Path(self.target_dir)
            
            if not source.exists():
                self.log_signal.emit("ERROR: Source directory does not exist")
                self.finished_signal.emit(False)
                return
            
            target.mkdir(parents=True, exist_ok=True)
            
            files_copied = 0
            files_skipped = 0
            
            for item in source.rglob("*"):
                try:
                    if item.is_file():
                        relative_path = item.relative_to(source)
                        
                        if self.should_skip(item.name):
                            files_skipped += 1
                            continue
                        
                        target_path = target / relative_path
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        shutil.copy2(item, target_path)
                        files_copied += 1
                        
                        if files_copied % 100 == 0:
                            self.log_signal.emit(f"Copied {files_copied} files...")
                
                except Exception:
                    continue
            
            self.log_signal.emit(f"Completed! Copied {files_copied} files, Skipped {files_skipped} files")
            self.finished_signal.emit(True)
            
        except Exception as e:
            self.log_signal.emit(f"ERROR: {str(e)}")
            self.finished_signal.emit(False)
    
    def should_skip(self, filename: str) -> bool:
        skip_items = {
            '.git', '.gitignore', '.gitattributes',
            '.idea', '.vscode', '.vs',
            '__pycache__', '.pytest_cache',
            'node_modules', '.npm',
            'venv', '.venv', 'env',
            'dist', 'build', 'target',
            '.DS_Store', 'Thumbs.db',
            'desktop.ini', '*.log'
        }
        
        for item in skip_items:
            if item.startswith('*.'):
                if filename.endswith(item[1:]):
                    return True
            elif filename == item:
                return True
        
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cleaning_thread = None
        self.project_file_count = 0
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        self.setWindowTitle("RepoPrep v1.0.0")
        self.setMinimumSize(900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.create_menu_bar()
        
        source_group = QGroupBox("Source Project")
        source_layout = QGridLayout()
        
        self.source_label = QLabel("Source Directory:")
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Select source project directory...")
        self.source_button = QPushButton("Browse...")
        self.source_button.clicked.connect(self.select_source_directory)
        
        self.source_info = QLabel("No project selected")
        self.source_info.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        
        source_layout.addWidget(self.source_label, 0, 0)
        source_layout.addWidget(self.source_input, 0, 1)
        source_layout.addWidget(self.source_button, 0, 2)
        source_layout.addWidget(self.source_info, 1, 0, 1, 3)
        
        source_group.setLayout(source_layout)
        
        target_group = QGroupBox("Clean Copy Location")
        target_layout = QGridLayout()
        
        self.target_label = QLabel("Target Directory:")
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Select where to save clean copy...")
        self.target_button = QPushButton("Browse...")
        self.target_button.clicked.connect(self.select_target_directory)
        
        target_layout.addWidget(self.target_label, 0, 0)
        target_layout.addWidget(self.target_input, 0, 1)
        target_layout.addWidget(self.target_button, 0, 2)
        
        target_group.setLayout(target_layout)
        
        scan_layout = QHBoxLayout()
        self.scan_button = QPushButton("Scan Project Files")
        self.scan_button.clicked.connect(self.scan_project_files)
        self.scan_button.setEnabled(False)
        
        scan_layout.addStretch()
        scan_layout.addWidget(self.scan_button)
        scan_layout.addStretch()
        
        self.clean_button = QPushButton("Clean & Copy Project")
        self.clean_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
                border-radius: 8px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.clean_button.clicked.connect(self.start_cleaning)
        self.clean_button.setEnabled(False)
        
        log_group = QGroupBox("Processing Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(250)
        
        clear_button = QPushButton("Clear Log")
        clear_button.clicked.connect(self.clear_log)
        
        log_layout.addWidget(self.log_text)
        log_layout.addWidget(clear_button)
        
        log_group.setLayout(log_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Select a project to start")
        
        main_layout.addWidget(source_group)
        main_layout.addWidget(target_group)
        main_layout.addLayout(scan_layout)
        main_layout.addWidget(self.clean_button)
        main_layout.addWidget(log_group)
        main_layout.addWidget(self.progress_bar)
        
        self.source_input.textChanged.connect(self.validate_inputs)
        self.target_input.textChanged.connect(self.validate_inputs)
        
        self.log("RepoPrep v1.0.0 started successfully!")
        self.log("Select a project directory and click 'Scan Project Files' to begin.")
    
    def create_menu_bar(self):
        menu_bar = QMenuBar()
        
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        self.setMenuBar(menu_bar)
    
    def apply_styles(self):
        self.setStyleSheet(STYLESHEET)
    
    @Slot()
    def select_source_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Source Project Directory",
            str(Path.home()),
            QFileDialog.ShowDirsOnly
        )
        
        if directory:
            self.source_input.setText(directory)
            self.source_info.setText(f"Selected: {directory}")
            self.scan_button.setEnabled(True)
            self.log(f"Source directory selected: {directory}")
    
    @Slot()
    def select_target_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Target Directory",
            str(Path.home()),
            QFileDialog.ShowDirsOnly
        )
        
        if directory:
            self.target_input.setText(directory)
            self.log(f"Target directory selected: {directory}")
    
    @Slot()
    def scan_project_files(self):
        source_dir = self.source_input.text().strip()
        
        if not source_dir or not os.path.exists(source_dir):
            QMessageBox.warning(self, "Error", "Please select a valid source directory first!")
            return
        
        try:
            path = Path(source_dir)
            file_count = 0
            total_size = 0
            
            for item in path.rglob("*"):
                if item.is_file():
                    try:
                        file_count += 1
                        total_size += item.stat().st_size
                    except:
                        continue
            
            self.project_file_count = file_count
            size_mb = total_size / (1024 * 1024)
            
            info_text = f"Project: {path.name} | "
            info_text += f"Files: {file_count:,} | "
            info_text += f"Size: {size_mb:.1f} MB"
            
            self.source_info.setText(info_text)
            self.log(f"Project scanned: {file_count:,} files found ({size_mb:.1f} MB)")
            self.status_bar.showMessage(f"Found {file_count:,} files in project")
            
        except Exception as e:
            self.log(f"ERROR scanning project: {str(e)}")
    
    @Slot()
    def validate_inputs(self):
        source = self.source_input.text().strip()
        target = self.target_input.text().strip()
        
        if source and target and source != target:
            self.clean_button.setEnabled(True)
        else:
            self.clean_button.setEnabled(False)
    
    @Slot()
    def start_cleaning(self):
        source_dir = self.source_input.text().strip()
        target_dir = self.target_input.text().strip()
        
        if not os.path.exists(source_dir):
            QMessageBox.warning(self, "Error", "Source directory does not exist!")
            return
        
        if source_dir == target_dir:
            QMessageBox.warning(self, "Error", "Source and target directories cannot be the same!")
            return
        
        try:
            source_path = Path(source_dir).resolve()
            target_path = Path(target_dir).resolve()
            
            if target_path.is_relative_to(source_path):
                QMessageBox.warning(self, "Error", "Target directory cannot be inside source directory!")
                return
        except:
            pass
        
        if os.path.exists(target_dir) and os.listdir(target_dir):
            reply = QMessageBox.question(
                self, "Confirm",
                "Target directory is not empty. Continue?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
        
        self.set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_bar.showMessage("Cleaning in progress...")
        
        self.log_text.clear()
        self.log("=" * 50)
        self.log("Starting cleaning process...")
        self.log(f"Source: {source_dir}")
        self.log(f"Target: {target_dir}")
        self.log(f"Project files: {self.project_file_count:,}")
        self.log("=" * 50)
        
        self.cleaning_thread = CleaningThread(source_dir, target_dir)
        self.cleaning_thread.log_signal.connect(self.log)
        self.cleaning_thread.finished_signal.connect(self.cleaning_finished)
        self.cleaning_thread.start()
    
    @Slot(bool)
    def cleaning_finished(self, success: bool):
        self.set_ui_enabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            self.status_bar.showMessage("Cleaning completed successfully!")
            QMessageBox.information(self, "Success", 
                "Project cleaned and copied successfully!")
        else:
            self.status_bar.showMessage("Cleaning failed!")
            QMessageBox.warning(self, "Error", 
                "Cleaning failed. Check logs for details.")
    
    def set_ui_enabled(self, enabled: bool):
        self.source_input.setEnabled(enabled)
        self.source_button.setEnabled(enabled)
        self.target_input.setEnabled(enabled)
        self.target_button.setEnabled(enabled)
        self.scan_button.setEnabled(enabled and bool(self.source_input.text()))
        self.clean_button.setEnabled(enabled and 
            bool(self.source_input.text() and self.target_input.text()))
    
    @Slot(str)
    def log(self, message: str):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    @Slot()
    def clear_log(self):
        self.log_text.clear()
        self.log("Log cleared")
    
    @Slot()
    def show_about(self):
        about_text = """
        <h2>RepoPrep v1.0.0</h2>
        <p>Professional Project Cleaner</p>
        
        <p>Clean and prepare your software projects for sharing and publishing.</p>
        
        <p><b>Features:</b></p>
        <ul>
            <li>Remove unnecessary files and folders</li>
            <li>Skip hidden and cache files</li>
            <li>Create clean copies of projects</li>
            <li>Detailed file scanning</li>
            <li>Progress logging</li>
        </ul>
        
        <p><b>Author:</b> Ryder</p>
        <p><b>Version:</b> 1.0.0</p>
        
        <p style="color: #888;">&copy; 2026 All rights reserved.</p>
        """
        
        QMessageBox.about(self, "About RepoPrep", about_text)
    
    def closeEvent(self, event):
        if self.cleaning_thread and self.cleaning_thread.isRunning():
            reply = QMessageBox.question(
                self, "Warning",
                "Cleaning is in progress. Are you sure you want to quit?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.cleaning_thread.terminate()
                self.cleaning_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()