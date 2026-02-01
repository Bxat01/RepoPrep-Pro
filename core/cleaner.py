import os
import shutil
from pathlib import Path
from datetime import datetime

class ProjectCleaner:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.copied_files = 0
        self.skipped_files = 0
    
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        if self.log_callback:
            self.log_callback(log_message)
        else:
            print(log_message)
    
    def clean_and_copy(self, source_dir: str, target_dir: str) -> bool:
        try:
            source = Path(source_dir)
            target = Path(target_dir)
            
            if not source.exists():
                self.log("Source directory not found", "ERROR")
                return False
            
            if source.resolve() == target.resolve():
                self.log("Cannot copy to same directory", "ERROR")
                return False
            
            target.mkdir(parents=True, exist_ok=True)
            
            self.copied_files = 0
            self.skipped_files = 0
            
            self._copy_directory(source, target, source)
            
            self.log(f"Operation completed: {self.copied_files} files copied, {self.skipped_files} files skipped")
            return True
            
        except Exception as e:
            self.log(f"Error: {str(e)}", "ERROR")
            return False
    
    def _copy_directory(self, source: Path, target: Path, root: Path):
        try:
            target.mkdir(exist_ok=True)
            
            for item in source.iterdir():
                try:
                    relative_path = item.relative_to(root)
                    
                    if self._should_skip(item):
                        self.skipped_files += 1
                        self.log(f"Skipped: {relative_path}", "SKIP")
                        continue
                    
                    if item.is_dir():
                        new_target = target / item.name
                        self._copy_directory(item, new_target, root)
                    elif item.is_file():
                        target_file = target / item.name
                        shutil.copy2(item, target_file)
                        self.copied_files += 1
                        
                        if self.copied_files % 100 == 0:
                            self.log(f"Copied {self.copied_files} files...")
                
                except Exception as e:
                    continue
                    
        except Exception as e:
            raise
    
    def _should_skip(self, item: Path) -> bool:
        skip_items = {
            '.git', '.svn', '.hg',
            '.idea', '.vscode', '.vs',
            '__pycache__', '.pytest_cache',
            'node_modules', '.npm', '.yarn',
            'dist', 'build', 'target',
            '.DS_Store', 'Thumbs.db',
            'desktop.ini', '*.log', '*.tmp'
        }
        
        name = item.name
        for pattern in skip_items:
            if pattern.startswith('*.'):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
        
        return False