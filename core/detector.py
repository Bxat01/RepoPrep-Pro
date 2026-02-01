import os
from pathlib import Path

class ProjectDetector:
    @staticmethod
    def detect_project_type(project_path: str) -> str:
        path = Path(project_path)
        
        if not path.exists():
            return "unknown"
        
        if (path / "package.json").exists():
            return "nodejs"
        elif (path / "requirements.txt").exists() or (path / "setup.py").exists():
            return "python"
        elif (path / "pom.xml").exists():
            return "java"
        elif (path / "pubspec.yaml").exists():
            return "flutter"
        elif (path / "composer.json").exists():
            return "php"
        elif (path / "Gemfile").exists():
            return "ruby"
        elif (path / "go.mod").exists():
            return "go"
        elif (path / "Cargo.toml").exists():
            return "rust"
        elif (path / ".csproj").exists() or (path / ".sln").exists():
            return "dotnet"
        
        return "unknown"
    
    @staticmethod
    def count_project_files(project_path: str) -> dict:
        path = Path(project_path)
        result = {
            "files": 0,
            "folders": 0,
            "size_bytes": 0,
            "ignored": 0
        }
        
        if not path.exists():
            return result
        
        ignore_patterns = ['.git', '__pycache__', 'node_modules', 'venv', '.venv', 'dist', 'build']
        
        for item in path.rglob("*"):
            try:
                if any(pattern in str(item) for pattern in ignore_patterns):
                    result["ignored"] += 1
                    continue
                
                if item.is_file():
                    result["files"] += 1
                    result["size_bytes"] += item.stat().st_size
                elif item.is_dir():
                    result["folders"] += 1
                    
            except (PermissionError, OSError):
                continue
        
        return result