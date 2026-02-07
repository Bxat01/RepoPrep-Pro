import os
from pathlib import Path

class ProjectDetector:
    """Detect project type and analyze project structure"""
    
    @staticmethod
    def detect_project_type(project_path: str) -> str:
        """Detect the type of project based on configuration files"""
        path = Path(project_path)
        
        if not path.exists():
            return "unknown"
        
        # Check for specific project type indicators
        if (path / "package.json").exists():
            return "Node.js/JavaScript"
        elif (path / "requirements.txt").exists() or (path / "setup.py").exists() or (path / "pyproject.toml").exists():
            return "Python"
        elif (path / "pom.xml").exists():
            return "Java Maven"
        elif (path / "build.gradle").exists() or (path / "settings.gradle").exists():
            return "Java Gradle"
        elif (path / "pubspec.yaml").exists():
            return "Flutter/Dart"
        elif (path / "composer.json").exists():
            return "PHP Composer"
        elif (path / "Gemfile").exists():
            return "Ruby Bundler"
        elif (path / "go.mod").exists():
            return "Go"
        elif (path / "Cargo.toml").exists():
            return "Rust Cargo"
        elif (path / ".csproj").exists() or (path / ".sln").exists():
            return ".NET/C#"
        elif (path / "package-lock.json").exists() or (path / "yarn.lock").exists():
            return "Node.js/JavaScript (Lock file)"
        elif (path / "Makefile").exists():
            return "C/C++"
        elif (path / "CMakeLists.txt").exists():
            return "CMake Project"
        
        return "Generic Project"
    
    @staticmethod
    def count_project_files(project_path: str) -> dict:
        """Count files, folders, and size with detailed breakdown"""
        path = Path(project_path)
        result = {
            "total_files": 0,
            "total_folders": 0,
            "total_size_bytes": 0,
            "total_size_mb": 0,
            "ignored_items": 0,
            "project_type": ProjectDetector.detect_project_type(project_path),
            "largest_dirs": []
        }
        
        if not path.exists():
            return result
        
        # Common directories to skip during analysis
        ignore_patterns = ['.git', '__pycache__', 'node_modules', 'venv', '.venv', 
                          'dist', 'build', 'target', '.idea', '.vscode', '.pytest_cache']
        
        # Track directory sizes for analysis
        dir_sizes = {}
        
        try:
            for item in path.rglob("*"):
                try:
                    # Check if item matches ignore patterns
                    if any(pattern in str(item) for pattern in ignore_patterns):
                        result["ignored_items"] += 1
                        continue
                    
                    if item.is_file():
                        result["total_files"] += 1
                        try:
                            file_size = item.stat().st_size
                            result["total_size_bytes"] += file_size
                            
                            # Track parent directory size
                            parent = item.parent.name
                            if parent not in dir_sizes:
                                dir_sizes[parent] = 0
                            dir_sizes[parent] += file_size
                        except:
                            pass
                    
                    elif item.is_dir():
                        result["total_folders"] += 1
                
                except (PermissionError, OSError):
                    continue
        
        except Exception as e:
            pass
        
        # Convert bytes to MB
        result["total_size_mb"] = round(result["total_size_bytes"] / (1024 * 1024), 2)
        
        return result
    
    @staticmethod
    def get_cleanup_estimate(project_path: str) -> dict:
        """Estimate how much space can be freed"""
        path = Path(project_path)
        estimate = {
            "node_modules_size": 0,
            "venv_size": 0,
            "cache_size": 0,
            "build_size": 0,
            "total_saveable_bytes": 0,
            "total_saveable_mb": 0
        }
        
        if not path.exists():
            return estimate
        
        try:
            # Check for node_modules
            node_modules = path / "node_modules"
            if node_modules.exists():
                estimate["node_modules_size"] = ProjectDetector._get_dir_size(node_modules)
            
            # Check for venv
            for venv_dir in ["venv", ".venv", "env", ".env"]:
                venv_path = path / venv_dir
                if venv_path.exists():
                    estimate["venv_size"] += ProjectDetector._get_dir_size(venv_path)
            
            # Check for cache directories
            for cache_dir in [".pytest_cache", ".mypy_cache", ".coverage", "__pycache__"]:
                cache_path = path / cache_dir
                if cache_path.exists():
                    estimate["cache_size"] += ProjectDetector._get_dir_size(cache_path)
            
            # Check for build directories
            for build_dir in ["build", "dist", "target", "out"]:
                build_path = path / build_dir
                if build_path.exists():
                    estimate["build_size"] += ProjectDetector._get_dir_size(build_path)
            
            estimate["total_saveable_bytes"] = (estimate["node_modules_size"] + 
                                               estimate["venv_size"] + 
                                               estimate["cache_size"] + 
                                               estimate["build_size"])
            estimate["total_saveable_mb"] = round(estimate["total_saveable_bytes"] / (1024 * 1024), 2)
        
        except Exception:
            pass
        
        return estimate
    
    @staticmethod
    def _get_dir_size(dir_path: Path) -> int:
        """Calculate total size of a directory"""
        total_size = 0
        try:
            for item in dir_path.rglob("*"):
                try:
                    if item.is_file():
                        total_size += item.stat().st_size
                except:
                    pass
        except:
            pass
        return total_size