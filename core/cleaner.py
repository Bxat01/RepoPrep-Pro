import os
import shutil
from pathlib import Path
from datetime import datetime
import gc

class ProjectCleaner:
    """Project cleaner with advanced error handling and memory optimization"""
    
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.copied_files = 0
        self.skipped_files = 0
        self.deleted_dirs = 0
        # Comprehensive skip patterns for all common package managers and build systems
        self.skip_dirs = {
            '.git', '.svn', '.hg', '.bzr',
            '.idea', '.vscode', '.vs', '.sublime-project', '.sublime-workspace',
            '__pycache__', '.pytest_cache', '.mypy_cache', '.coverage',
            'node_modules', '.npm', '.yarn', '.pnp', '.pnp.js',
            'dist', 'build', 'target', 'out', 'bin', 'obj',
            'venv', '.venv', 'env', '.env', 'ENV',
            '.egg-info', '.eggs', '.tox', '.hypothesis',
            'vendor', 'packages', '.gradle', '.m2',
            '.DS_Store', '.AppleDouble', '.LSOverride',
            'site-packages', 'dist-packages',
            'Pods', '.xcworkspace',
            'next', '.next', '.nuxt', '.gatsby',
            'coverage', '.nyc_output',
        }
        
        self.skip_files = {
            '.DS_Store', 'Thumbs.db', 'desktop.ini',
            '.gitkeep', '.keep', '.env.local',
        }
        
        self.skip_extensions = {
            '.log', '.tmp', '.bak', '.swp', '.swo',
            '.pyc', '.pyo', '.pyd', '.so',
            '.class', '.jar', '.dll', '.exe',
            '.o', '.a', '.lib', '.lock',
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [{level:5s}] {message}"
        
        if self.log_callback:
            self.log_callback(log_message)
        else:
            print(log_message)
    
    def clean_and_copy(self, source_dir: str, target_dir: str) -> bool:
        """Clean and copy project with comprehensive error handling"""
        try:
            source = Path(source_dir)
            target = Path(target_dir)
            
            # Validation
            if not source.exists():
                self.log("Source directory not found", "ERROR")
                return False
            
            if not source.is_dir():
                self.log("Source path is not a directory", "ERROR")
                return False
            
            try:
                if source.resolve() == target.resolve():
                    self.log("Cannot copy to same directory", "ERROR")
                    return False
            except Exception:
                pass
            
            # Create target
            try:
                target.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.log(f"Failed to create target directory: {str(e)}", "ERROR")
                return False
            
            # Reset counters
            self.copied_files = 0
            self.skipped_files = 0
            self.deleted_dirs = 0
            
            self.log("Starting project cleaning and copying...", "INFO")
            
            # Perform copy
            try:
                self._copy_directory_safe(source, target, source)
            except Exception as e:
                self.log(f"Error during copying: {str(e)}", "ERROR")
                return False
            
            # Cleanup memory
            gc.collect()
            
            self.log(f"Operation completed: {self.copied_files} files copied, {self.skipped_files} files/dirs skipped", "INFO")
            return True
            
        except Exception as e:
            self.log(f"Critical error: {str(e)}", "ERROR")
            return False
    
    def _copy_directory_safe(self, source: Path, target: Path, root: Path):
        """Safely copy directory with memory optimization"""
        try:
            target.mkdir(exist_ok=True)
        except Exception as e:
            self.log(f"Cannot create directory {target.name}: {str(e)}", "WARN")
            return
        
        try:
            items = list(source.iterdir())
        except PermissionError:
            self.log(f"Permission denied accessing {source.name}", "WARN")
            return
        except Exception as e:
            self.log(f"Error reading directory {source.name}: {str(e)}", "WARN")
            return
        
        for item in items:
            try:
                relative_path = item.relative_to(root)
                
                if self._should_skip(item):
                    self.skipped_files += 1
                    self.log(f"Skipped: {relative_path}", "SKIP")
                    continue
                
                if item.is_symlink():
                    self.log(f"Skipped symlink: {relative_path}", "SKIP")
                    self.skipped_files += 1
                    continue
                
                if item.is_dir():
                    new_target = target / item.name
                    try:
                        self._copy_directory_safe(item, new_target, root)
                    except Exception as e:
                        self.log(f"Error processing directory {item.name}: {str(e)}", "WARN")
                        continue
                
                elif item.is_file():
                    try:
                        target_file = target / item.name
                        shutil.copy2(item, target_file, follow_symlinks=False)
                        self.copied_files += 1
                        
                        if self.copied_files % 500 == 0:
                            self.log(f"Progress: {self.copied_files} files copied...", "INFO")
                            gc.collect()  # Memory optimization
                    
                    except PermissionError:
                        self.log(f"Permission denied copying {item.name}", "WARN")
                        self.skipped_files += 1
                    except Exception as e:
                        self.log(f"Error copying {item.name}: {str(e)}", "WARN")
                        self.skipped_files += 1
            
            except Exception as e:
                self.log(f"Error processing item: {str(e)}", "WARN")
                self.skipped_files += 1
    
    def _should_skip(self, item: Path) -> bool:
        """Check if item should be skipped"""
        name = item.name
        
        # Skip hidden files on Unix
        if name.startswith('.'):
            if name in self.skip_dirs or name in self.skip_files:
                return True
            # Skip by extension
            if any(name.endswith(ext) for ext in self.skip_extensions):
                return True
        
        # Check directory names
        if item.is_dir() and name in self.skip_dirs:
            return True
        
        # Check file names
        if item.is_file():
            if name in self.skip_files:
                return True
            # Check extensions
            if any(name.endswith(ext) for ext in self.skip_extensions):
                return True
        
        return False
    
    def get_stats(self) -> dict:
        """Get cleaning statistics"""
        return {
            'files_copied': self.copied_files,
            'items_skipped': self.skipped_files,
            'dirs_deleted': self.deleted_dirs,
        }