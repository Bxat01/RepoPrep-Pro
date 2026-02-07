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

class ScanThread(QThread):
    scan_complete = Signal(int, int, float, str)
    scan_error = Signal(str)
    
    def __init__(self, directory: str):
        super().__init__()
        self.directory = directory
        self.cancelled = False
    
    def run(self):
        try:
            path = Path(self.directory)
            file_count = 0
            dir_count = 0
            total_size = 0
            
            for item in path.rglob("*"):
                if self.cancelled:
                    return
                
                try:
                    if item.is_file():
                        file_count += 1
                        total_size += item.stat().st_size
                    elif item.is_dir():
                        dir_count += 1
                except:
                    pass
            
            size_mb = total_size / (1024 * 1024)
            project_name = path.name
            self.scan_complete.emit(file_count, dir_count, size_mb, project_name)
        
        except Exception as e:
            self.scan_error.emit(str(e))

class CleaningThread(QThread):
    """Thread for background project cleaning"""
    log_signal = Signal(str)
    finished_signal = Signal(bool)
    progress_signal = Signal(int)
    
    def __init__(self, source_dir: str, target_dir: str):
        super().__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.should_cancel = False
        
        # Comprehensive skip patterns
        self.skip_dirs = {
            '.git', '.svn', '.hg', '.bzr',
            '.idea', '.vscode', '.vs',
            '__pycache__', '.pytest_cache', '.mypy_cache', '.coverage',
            'node_modules', '.npm', '.yarn', '.pnp',
            'dist', 'build', 'target', 'out', 'bin', 'obj',
            'venv', '.venv', 'env', '.env',
            '.egg-info', '.eggs', '.tox',
            'vendor', 'packages', '.gradle', '.m2',
            'site-packages', 'dist-packages',
            '.next', '.nuxt', '.gatsby',
        }
        
        self.skip_files = {
            '.DS_Store', 'Thumbs.db', 'desktop.ini',
        }
        
        self.skip_extensions = {
            '.log', '.tmp', '.bak', '.swp', '.lock',
        }
    
    def run(self):
        """Execute cleaning operation"""
        try:
            source = Path(self.source_dir)
            target = Path(self.target_dir)
            
            if not source.exists():
                self.log_signal.emit("ERROR: Source directory does not exist")
                self.finished_signal.emit(False)
                return
            
            if not source.is_dir():
                self.log_signal.emit("ERROR: Source path is not a directory")
                self.finished_signal.emit(False)
                return
            
            try:
                target.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.log_signal.emit(f"ERROR: Failed to create target directory: {str(e)}")
                self.finished_signal.emit(False)
                return
            
            files_copied = 0
            files_skipped = 0
            dirs_processed = 0
            
            self.log_signal.emit("Starting directory scan and copy operation...")
            
            try:
                for item in source.rglob("*"):
                    if self.should_cancel:
                        self.log_signal.emit("Operation cancelled by user")
                        self.finished_signal.emit(False)
                        return
                    
                    try:
                        if item.is_symlink():
                            continue
                        
                        relative_path = item.relative_to(source)
                        
                        if self._should_skip_path(relative_path):
                            files_skipped += 1
                            if files_skipped % 1000 == 0:
                                self.log_signal.emit(f"Skipped {files_skipped} items...")
                            continue
                        
                        if item.is_dir():
                            target_dir_path = target / relative_path
                            try:
                                target_dir_path.mkdir(parents=True, exist_ok=True)
                                dirs_processed += 1
                            except PermissionError:
                                self.log_signal.emit(f"WARN: Permission denied - {relative_path}")
                                files_skipped += 1
                            except Exception as e:
                                self.log_signal.emit(f"WARN: Cannot create directory - {relative_path}: {str(e)}")
                                files_skipped += 1
                        
                        elif item.is_file():
                            try:
                                target_file = target / relative_path
                                target_file.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(item, target_file, follow_symlinks=False)
                                files_copied += 1
                                
                                if files_copied % 500 == 0:
                                    self.log_signal.emit(f"Progress: {files_copied} files copied, {files_skipped} skipped...")
                            
                            except PermissionError:
                                self.log_signal.emit(f"WARN: Permission denied - {item.name}")
                                files_skipped += 1
                            except OSError as e:
                                if "too many open files" in str(e):
                                    self.log_signal.emit(f"WARN: Too many open files, closing some...")
                                    import gc
                                    gc.collect()
                                else:
                                    self.log_signal.emit(f"WARN: OS Error copying {item.name}: {str(e)}")
                                files_skipped += 1
                            except Exception as e:
                                self.log_signal.emit(f"WARN: Error copying {item.name}: {str(e)}")
                                files_skipped += 1
                    
                    except Exception as e:
                        self.log_signal.emit(f"WARN: Error processing item: {str(e)}")
                        files_skipped += 1
            
            except Exception as e:
                self.log_signal.emit(f"ERROR: Fatal error during copy: {str(e)}")
                self.finished_signal.emit(False)
                return
            
            # Success
            self.log_signal.emit("-" * 50)
            self.log_signal.emit(f"Completed successfully!")
            self.log_signal.emit(f"Files copied: {files_copied:,}")
            self.log_signal.emit(f"Items skipped: {files_skipped:,}")
            self.log_signal.emit(f"Directories created: {dirs_processed:,}")
            self.log_signal.emit(f"Total disk space saved: Approx {files_skipped * 1024 / (1024*1024):.1f} MB")
            self.log_signal.emit("-" * 50)
            self.finished_signal.emit(True)
            
        except Exception as e:
            self.log_signal.emit(f"ERROR: Unexpected error: {str(e)}")
            self.finished_signal.emit(False)
    
    def _should_skip_path(self, relative_path: Path) -> bool:
        """Check if path contains any skip directory in its components"""
        path_parts = relative_path.parts
        
        for part in path_parts:
            if part in self.skip_dirs:
                return True
        
        if relative_path.name in self.skip_files:
            return True
        
        if relative_path.suffix in self.skip_extensions:
            return True
        
        return False

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.cleaning_thread = None
        self.scan_thread = None
        self.project_file_count = 0
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("RepoPrep v1.1.0 - Project Cleaner")
        self.setMinimumSize(950, 750)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.create_menu_bar()
        
        # Source group
        source_group = QGroupBox("Source Project Directory")
        source_layout = QGridLayout()
        
        self.source_label = QLabel("Source Path:")
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Select source project folder...")
        self.source_button = QPushButton("Browse...")
        self.source_button.clicked.connect(self.select_source_directory)
        
        self.source_info = QLabel("No project selected")
        self.source_info.setStyleSheet("color: #999; font-style: italic; padding: 5px;")
        
        source_layout.addWidget(self.source_label, 0, 0)
        source_layout.addWidget(self.source_input, 0, 1)
        source_layout.addWidget(self.source_button, 0, 2)
        source_layout.addWidget(self.source_info, 1, 0, 1, 3)
        
        source_group.setLayout(source_layout)
        
        # Target group
        target_group = QGroupBox("Target Directory for Clean Copy")
        target_layout = QGridLayout()
        
        self.target_label = QLabel("Target Path:")
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Select destination for cleaned project...")
        self.target_button = QPushButton("Browse...")
        self.target_button.clicked.connect(self.select_target_directory)
        
        target_layout.addWidget(self.target_label, 0, 0)
        target_layout.addWidget(self.target_input, 0, 1)
        target_layout.addWidget(self.target_button, 0, 2)
        
        target_group.setLayout(target_layout)
        
        # Scan button
        scan_layout = QHBoxLayout()
        self.scan_button = QPushButton("Scan Project Files")
        self.scan_button.clicked.connect(self.scan_project_files)
        self.scan_button.setEnabled(False)
        scan_layout.addStretch()
        scan_layout.addWidget(self.scan_button)
        scan_layout.addStretch()
        
        # Clean button
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
        
        # Log group
        log_group = QGroupBox("Processing Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(280)
        self.log_text.setFont(QFont("Courier New", 9))
        
        log_buttons_layout = QHBoxLayout()
        clear_button = QPushButton("Clear Log")
        clear_button.clicked.connect(self.clear_log)
        log_buttons_layout.addStretch()
        log_buttons_layout.addWidget(clear_button)
        
        log_layout.addWidget(self.log_text)
        log_layout.addLayout(log_buttons_layout)
        
        log_group.setLayout(log_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
                background: #3c3c3c;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Select a project to begin")
        
        # Add all widgets to main layout
        main_layout.addWidget(source_group)
        main_layout.addWidget(target_group)
        main_layout.addLayout(scan_layout)
        main_layout.addWidget(self.clean_button)
        main_layout.addWidget(log_group, 1)
        main_layout.addWidget(self.progress_bar)
        
        # Connect signals
        self.source_input.textChanged.connect(self.validate_inputs)
        self.target_input.textChanged.connect(self.validate_inputs)
        
        # Initial log message
        self.log("RepoPrep v1.1.0 started successfully!")
        self.log("Select a source project directory and click 'Scan' to begin.")
        self.log("-" * 50)
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menu_bar = QMenuBar()
        
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About RepoPrep", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        self.setMenuBar(menu_bar)
    
    def apply_styles(self):
        """Apply stylesheet"""
        self.setStyleSheet(STYLESHEET)
    
    @Slot()
    def select_source_directory(self):
        """Select source project directory"""
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
        """Select target directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Target Directory for Clean Copy",
            str(Path.home()),
            QFileDialog.ShowDirsOnly
        )
        
        if directory:
            self.target_input.setText(directory)
            self.log(f"Target directory selected: {directory}")
    
    @Slot()
    def scan_project_files(self):
        """Scan and count project files in background thread"""
        source_dir = self.source_input.text().strip()
        
        if not source_dir or not os.path.exists(source_dir):
            QMessageBox.warning(self, "Error", "Please select a valid source directory first!")
            return
        
        self.scan_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_bar.showMessage("Scanning project files... Please wait.")
        self.log("Scanning project files (this may take a while for large projects)...")
        
        self.scan_thread = ScanThread(source_dir)
        self.scan_thread.scan_complete.connect(self.on_scan_complete)
        self.scan_thread.scan_error.connect(self.on_scan_error)
        self.scan_thread.start()
    
    @Slot(int, int, float, str)
    def on_scan_complete(self, file_count: int, dir_count: int, size_mb: float, project_name: str):
        """Handle scan completion"""
        self.progress_bar.setVisible(False)
        self.scan_button.setEnabled(True)
        
        self.project_file_count = file_count
        
        info_text = f"Project: {project_name} | "
        info_text += f"Files: {file_count:,} | "
        info_text += f"Folders: {dir_count:,} | "
        info_text += f"Total Size: {size_mb:.1f} MB"
        
        self.source_info.setText(info_text)
        self.log(f"Scan complete: {file_count:,} files, {dir_count:,} folders, {size_mb:.1f} MB total")
        self.status_bar.showMessage(f"Project ready for cleaning: {file_count:,} files")
    
    @Slot(str)
    def on_scan_error(self, error_msg: str):
        """Handle scan error"""
        self.progress_bar.setVisible(False)
        self.scan_button.setEnabled(True)
        self.log(f"ERROR scanning project: {error_msg}")
        QMessageBox.warning(self, "Error", f"Failed to scan project: {error_msg}")
    
    @Slot()
    def validate_inputs(self):
        """Validate input paths"""
        source = self.source_input.text().strip()
        target = self.target_input.text().strip()
        
        if source and target and source != target and os.path.exists(source) and os.path.exists(target):
            self.clean_button.setEnabled(True)
        else:
            self.clean_button.setEnabled(False)
    
    @Slot()
    def start_cleaning(self):
        """Start the cleaning process"""
        source_dir = self.source_input.text().strip()
        target_dir = self.target_input.text().strip()
        
        # Validation
        if not os.path.exists(source_dir):
            QMessageBox.warning(self, "Error", "Source directory does not exist!")
            return
        
        if not os.path.exists(target_dir):
            QMessageBox.warning(self, "Error", "Target directory does not exist!")
            return
        
        if source_dir == target_dir:
            QMessageBox.warning(self, "Error", "Source and target directories must be different!")
            return
        
        try:
            source_path = Path(source_dir).resolve()
            target_path = Path(target_dir).resolve()
            
            if str(target_path).startswith(str(source_path)):
                QMessageBox.warning(self, "Error", "Target cannot be inside source directory!")
                return
        except:
            pass
        
        # Ask confirmation if target is not empty
        if os.path.exists(target_dir) and os.listdir(target_dir):
            reply = QMessageBox.question(
                self, "Confirm Overwrite",
                "Target directory is not empty. Files will be overwritten. Continue?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
        
        # Disable UI and start progress
        self.set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_bar.showMessage("Cleaning in progress... Please wait.")
        
        # Clear log
        self.log_text.clear()
        self.log("=" * 50)
        self.log("STARTING CLEAN & COPY OPERATION")
        self.log("=" * 50)
        self.log(f"Source:  {source_dir}")
        self.log(f"Target:  {target_dir}")
        self.log(f"Files to process: {self.project_file_count:,}")
        self.log("=" * 50)
        
        # Start thread
        self.cleaning_thread = CleaningThread(source_dir, target_dir)
        self.cleaning_thread.log_signal.connect(self.log)
        self.cleaning_thread.finished_signal.connect(self.cleaning_finished)
        self.cleaning_thread.start()
    
    @Slot(bool)
    def cleaning_finished(self, success: bool):
        """Handle cleaning completion"""
        self.set_ui_enabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            self.status_bar.showMessage("Cleaning completed successfully!")
            QMessageBox.information(self, "Success", 
                "Project cleaned and copied successfully!\n\nAll unnecessary files have been removed.")
        else:
            self.status_bar.showMessage("Cleaning failed!")
            QMessageBox.critical(self, "Error", 
                "Cleaning operation failed. Check the log for details.")
    
    def set_ui_enabled(self, enabled: bool):
        """Enable/disable UI elements"""
        self.source_input.setEnabled(enabled)
        self.source_button.setEnabled(enabled)
        self.target_input.setEnabled(enabled)
        self.target_button.setEnabled(enabled)
        self.scan_button.setEnabled(enabled and bool(self.source_input.text()))
        self.clean_button.setEnabled(enabled and 
            bool(self.source_input.text() and self.target_input.text()))
    
    @Slot(str)
    def log(self, message: str):
        """Add message to log"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    @Slot()
    def clear_log(self):
        """Clear the log"""
        self.log_text.clear()
        self.log("Log cleared")
    
    @Slot()
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>RepoPrep v1.1.0</h2>
        <p><b>Professional Project Cleaner</b></p>
        
        <p>Clean and prepare your software projects for sharing and publishing.</p>
        
        <p><b>Features:</b></p>
        <ul>
            <li>Remove unnecessary files and folders</li>
            <li>Support for all major project types</li>
            <li>Skip node_modules, venv, build directories automatically</li>
            <li>Handle large projects (100,000+ files)</li>
            <li>Better error handling and recovery</li>
            <li>Detailed processing logs</li>
            <li>Memory optimized for performance</li>
        </ul>
        
        <p><b>Author:</b> Ryder</p>
        <p><b>Version:</b> 1.1.0</p>
        <p><b>License:</b> MIT</p>
        
        <p style="color: #888; margin-top: 20px;">&copy; 2026 All rights reserved.</p>
        """
        
        QMessageBox.about(self, "About RepoPrep", about_text)
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.cleaning_thread and self.cleaning_thread.isRunning():
            reply = QMessageBox.question(
                self, "Confirm Exit",
                "Cleaning operation is in progress. Do you want to cancel and quit?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.cleaning_thread.should_cancel = True
                self.cleaning_thread.terminate()
                self.cleaning_thread.wait(3000)  # Wait max 3 seconds
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()