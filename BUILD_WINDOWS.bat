@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title RepoPrep - Quick Build
color 0E

cls
echo.
echo ╔══════════════════════════════════════════════╗
echo ║           RepoPrep - Build Tool            ║
echo ╚══════════════════════════════════════════════╝
echo.

:MAIN_MENU
cls
echo.
echo ╔══════════════════════════════════════════════╗
echo ║           RepoPrep - Main Menu              ║
echo ╚══════════════════════════════════════════════╝
echo.
echo Select an option:
echo.
echo [1] Check Python installation
echo [2] Install requirements
echo [3] Build executable (PyInstaller)
echo [4] Run application
echo [5] Open folder
echo [6] Exit
echo.
choice /c 123456 /n /m "Enter your choice (1-6): "

if errorlevel 6 goto :EXIT
if errorlevel 5 goto :OPEN_FOLDER
if errorlevel 4 goto :RUN_APP
if errorlevel 3 goto :BUILD
if errorlevel 2 goto :INSTALL
if errorlevel 1 goto :CHECK_PYTHON

:CHECK_PYTHON
cls
echo.
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.10+ from python.org
    echo Make sure to check "Add Python to PATH"
    echo.
) else (
    for /f "tokens=*" %%a in ('python --version 2^>^&1') do echo ✅ Python Found: %%a
    echo.
)
pause
goto MAIN_MENU

:INSTALL
cls
echo.
echo Installing requirements...
echo.
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ Failed to install requirements
    echo.
) else (
    echo.
    echo ✅ Requirements installed successfully
    echo.
)
pause
goto MAIN_MENU

:BUILD
cls
echo.
echo ╔══════════════════════════════════════════════╗
echo ║         Building Executable (PyInstaller)   ║
echo ╚══════════════════════════════════════════════╝
echo.

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    pause
    goto MAIN_MENU
)

echo Checking PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

echo Installing requirements...
python -m pip install -r requirements.txt

echo.
echo Cleaning old build...
if exist dist rmdir /s /q dist >nul 2>&1
if exist build rmdir /s /q build >nul 2>&1
if exist RepoPrep.spec del /q RepoPrep.spec >nul 2>&1

echo.
echo Building executable...
echo This may take 3-5 minutes...
echo.

python -m PyInstaller --onefile --windowed --name RepoPrep --icon=icon.ico --distpath=dist --workpath=build --add-data "ui;ui" --add-data "core;core" --add-data "translations;translations" --add-data "icon.ico;." --clean --noconfirm main.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    echo.
    pause
    goto MAIN_MENU
)

echo.
echo ✅ Build completed successfully!
echo.
if exist "dist\RepoPrep.exe" (
    for /f "usebackq" %%A in ('dist\RepoPrep.exe') do set /a size=%%~zA/1048576
    echo Location: dist\RepoPrep.exe
    echo Size: !size! MB
    echo.
)
pause
goto MAIN_MENU

:RUN_APP
cls
echo.
if exist "dist\RepoPrep.exe" (
    echo Starting RepoPrep...
    echo.
    start "" "dist\RepoPrep.exe"
    echo ✅ Application launched
    echo.
) else (
    echo ❌ RepoPrep.exe not found!
    echo Please build it first (Option 3).
    echo.
)
pause
goto MAIN_MENU

:OPEN_FOLDER
explorer .
goto MAIN_MENU

:EXIT
cls
echo.
echo Thank you for using RepoPrep!
echo.
timeout /t 2 >nul
exit /b 0
