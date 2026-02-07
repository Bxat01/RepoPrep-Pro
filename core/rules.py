"""
Comprehensive cleaning rules for different project types
"""

class CleanRules:
    """Cleaning rules for different project types"""
    
    @staticmethod
    def get_rules_for_project(project_type: str) -> dict:
        """Get cleaning rules for specific project type"""
        
        # Universal directories that should always be removed
        common_dirs = {
            # Version control
            ".git", ".svn", ".hg", ".bzr",
            
            # IDE configurations
            ".idea", ".vscode", ".vs", ".sublime-project", ".sublime-workspace",
            
            # Python
            "__pycache__", ".pytest_cache", ".mypy_cache", ".coverage",
            ".tox", ".hypothesis", ".eggs", ".egg-info",
            
            # Node.js
            "node_modules", ".npm", ".yarn", ".pnp", ".pnp.js",
            
            # Build artifacts
            "dist", "build", "target", "out", "bin", "obj",
            
            # Virtual environments
            "venv", ".venv", "env", ".env", "ENV",
            
            # Java/Gradle
            ".gradle", ".m2",
            
            # Ruby
            "Gemfile.lock",
            
            # Frontend
            ".next", ".nuxt", ".gatsby",
            
            # System
            ".DS_Store", ".AppleDouble", ".LSOverride",
        }
        
        # Universal files that should be removed
        common_files = {
            ".DS_Store", "Thumbs.db", "desktop.ini",
            ".gitkeep", ".keep",
        }
        
        # Add project-specific rules
        if "nodejs" in project_type.lower() or "javascript" in project_type.lower():
            common_dirs.update({".npm", ".yarn", ".next", ".nuxt"})
            common_files.update({"package-lock.json", "yarn.lock", "pnpm-lock.yaml"})
        
        elif "python" in project_type.lower():
            common_dirs.update({".pytest_cache", ".mypy_cache", ".coverage"})
            common_files.update({"*.pyc", ".coverage", "setup.py"})
        
        elif "java" in project_type.lower():
            common_dirs.update({".gradle", ".m2", "target"})
            common_files.update({"*.class", "*.jar"})
        
        elif "rust" in project_type.lower():
            common_dirs.update({"target"})
            common_files.update({"Cargo.lock"})
        
        elif "go" in project_type.lower():
            common_dirs.update({"vendor", ".go"})
        
        elif "ruby" in project_type.lower():
            common_files.update({"Gemfile.lock"})
        
        return {
            "directories": common_dirs,
            "files": common_files,
        }
    
    @staticmethod
    def get_all_skip_patterns() -> dict:
        """Get all skip patterns (directories, files, extensions)"""
        return {
            "directories": {
                ".git", ".svn", ".hg", ".bzr",
                ".idea", ".vscode", ".vs",
                "__pycache__", ".pytest_cache", ".mypy_cache",
                "node_modules", ".npm", ".yarn",
                "dist", "build", "target",
                "venv", ".venv", "env",
                ".DS_Store", ".AppleDouble",
                ".next", ".nuxt", ".gradle",
            },
            "files": {
                ".DS_Store", "Thumbs.db", "desktop.ini",
            },
            "extensions": {
                ".pyc", ".pyo", ".pyd", ".so",
                ".class", ".jar",
                ".log", ".tmp", ".bak",
                ".swp", ".swo",
                ".lock",
            }
        }
    
    @staticmethod
    def should_ignore(item, rules: dict) -> bool:
        """Check if item should be ignored based on rules"""
        from pathlib import Path
        
        item_path = Path(item) if isinstance(item, str) else item
        item_name = item_path.name
        
        if item_path.is_dir():
            return item_name in rules.get("directories", set())
        
        elif item_path.is_file():
            # Check file name
            if item_name in rules.get("files", set()):
                return True
            
            # Check file extensions
            for pattern in rules.get("files", set()):
                if pattern.startswith("*."):
                    if item_path.suffix == pattern[1:]:
                        return True
                elif item_path.name == pattern:
                    return True
        
        return False
    
    @staticmethod
    def should_skip(item_name: str, item_type: str = "file") -> bool:
        """Quick check if item should be skipped"""
        all_patterns = CleanRules.get_all_skip_patterns()
        
        if item_type == "dir" or item_type == "directory":
            return item_name in all_patterns["directories"]
        
        elif item_type == "file":
            if item_name in all_patterns["files"]:
                return True
            
            # Check extensions
            for ext in all_patterns["extensions"]:
                if item_name.endswith(ext):
                    return True
        
        return False