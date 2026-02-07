# RepoPrep v1.1.0 - Professional Project Cleaner

Clean and prepare your software projects for sharing, backup, or distribution.

## Features

✅ Smart Cleaning: Automatically removes unnecessary files and directories  
✅ Project Detection: Recognizes Node.js, Python, Java, Go, Rust, and more  
✅ Library Removal: Properly handles large package directories (node_modules, venv, etc.)  
✅ Safe Operation: Never modifies the original project  
✅ Detailed Logging: See exactly what's being processed  
✅ Large Project Support: Handles projects with 100,000+ files  
✅ Memory Optimized: Efficient processing without crashes  

## System Requirements

- Windows 10/11 (64-bit)
- Python 3.10+ (if running from source)
- 4 GB RAM minimum
- 200 MB free disk space

## Quick Start

### Run from Source
```bash
pip install -r requirements.txt
python main.py
```

### Build Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name RepoPrep --icon=icon.ico main.py
```

## Files Removed

- .git, .svn, .hg - Version control
- node_modules, venv, .venv, env - Dependencies
- __pycache__, .pytest_cache, .mypy_cache - Cache files
- dist, build, target - Build artifacts
- .idea, .vscode, .vs - IDE configuration
- .DS_Store, Thumbs.db - System files
- *.log, *.tmp - Temporary files

## License

MIT License © 2026 RyderDev

text

## 7. Creating a run.bat file for quick execution
```batch
@echo off
chcp 65001 >nul
echo ========================================
echo    RepoPrep Pro v2.0 (2026)
echo    Professional Project Cleaner
echo ========================================
echo.
```
REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt >nul 2>&1

REM Run application
echo Starting RepoPrep Pro...
python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start application
    pause
)

