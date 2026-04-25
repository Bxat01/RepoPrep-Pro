@echo off
chcp 65001 >nul
title RepoPrep Pro v2 — Lidprex Labs — Build

echo.
echo  ========================================
echo     RepoPrep Pro v2 - Lidprex Labs
echo             Build Tool
echo  ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
echo [ERROR] Python not found.
pause
exit /b 1
)

if not exist "icon.ico" (
echo [WARNING] icon.ico not found!
echo.
)

echo [1/3] Installing PyInstaller...
python -m pip install pyinstaller -q

echo [2/3] Cleaning previous build...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist "RepoPrep-Pro.spec" del /q "RepoPrep-Pro.spec"

echo [3/3] Building executable...
set "ICON_PARAM="
if exist "icon.ico" set ICON_PARAM=--icon="icon.ico" --add-data="icon.ico;."

python -m PyInstaller --onefile --windowed --name "RepoPrep-Pro" %ICON_PARAM% --clean --noconfirm main.py

if exist "dist\RepoPrep-Pro.exe" (
echo.
echo [OK] Build Successful!
echo.
explorer dist
) else (
echo.
echo [FAIL] Build failed.
)
pause