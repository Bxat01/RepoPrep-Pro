"""
Cleaning Rules
"""

class CleanRules:
    """Cleaning rules for projects"""
    
    @staticmethod
    def get_rules_for_project(project_type: str) -> dict:
        """Get rules for specific project type"""
        # Common rules for all projects
        common_dirs = {
            ".git", ".idea", ".vscode", ".vs",
            "__pycache__", "node_modules",
            "dist", "build", "target", "bin", "obj",
            "venv", ".venv", "env",
        }
        
        common_files = {
            ".DS_Store", "Thumbs.db", "desktop.ini",
            "*.log", "*.pyc", "*.class",
        }
        
        # Add project-specific rules
        if project_type == "nodejs":
            common_dirs.update({".npm", ".yarn", ".next"})
            common_files.update({"package-lock.json", "yarn.lock"})
        elif project_type == "python":
            common_dirs.update({".pytest_cache", ".mypy_cache"})
        elif project_type == "java":
            common_dirs.update({".gradle", "out"})
        
        return {
            "directories": common_dirs,
            "files": common_files,
        }
    
    @staticmethod
    def should_ignore(item, rules: dict) -> bool:
        """Check if item should be ignored"""
        from pathlib import Path
        item_path = Path(item) if isinstance(item, str) else item
        
        if item_path.is_dir():
            return item_path.name in rules["directories"]
        elif item_path.is_file():
            for pattern in rules["files"]:
                if pattern.startswith("*."):
                    if item_path.suffix == pattern[1:]:
                        return True
                elif item_path.name == pattern:
                    return True
        return False