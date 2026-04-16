@echo off
chcp 65001 >nul
title CppOS Quick Runner

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ======================================
echo   CppOS Quick Runner
echo ======================================
echo.
echo Current directory: %CD%
echo.

:: Check QEMU in PATH first
set "QEMU_CMD=qemu-system-i386"
where qemu-system-i386 >nul 2>&1
if %ERRORLEVEL% EQU 0 goto :qemu_found

:: Check common QEMU locations on Windows
echo [INFO] QEMU not in PATH, checking common locations...

set "QEMU_PATHS=C:\Program Files\qemu\qemu-system-i386.exe;C:\Program Files (x86)\qemu\qemu-system-i386.exe;C:\qemu\qemu-system-i386.exe;C:\msys64\mingw64\bin\qemu-system-i386.exe;C:\msys64\mingw32\bin\qemu-system-i386.exe"

for %%Q in (%QEMU_PATHS%) do (
    if exist "%%Q" (
        echo [OK] Found QEMU at: %%Q
        set "QEMU_CMD=%%Q"
        goto :qemu_found
    )
)

:: QEMU not found
echo.
echo [ERROR] QEMU not found!
echo.
echo QEMU is required to run CppOS.
echo.
echo Installation options:
echo   1. Download from: https://qemu.weilnetz.de/w64/
echo   2. Install with MSYS2: pacman -S qemu
echo   3. Add QEMU to your PATH environment variable
echo.
echo Opening download page...
start https://qemu.weilnetz.de/w64/
pause
exit /b 1

:qemu_found
echo [OK] QEMU: %QEMU_CMD%
echo.

:: Find kernel in multiple locations
echo [INFO] Searching for kernel...
set "KERNEL="

:: Check all possible locations
if exist "%SCRIPT_DIR%releases\cppos.bin" (
    set "KERNEL=%SCRIPT_DIR%releases\cppos.bin"
    goto :kernel_found
)
if exist "%SCRIPT_DIR%build\cppos.bin" (
    set "KERNEL=%SCRIPT_DIR%build\cppos.bin"
    goto :kernel_found
)
if exist "releases\cppos.bin" (
    set "KERNEL=releases\cppos.bin"
    goto :kernel_found
)
if exist "build\cppos.bin" (
    set "KERNEL=build\cppos.bin"
    goto :kernel_found
)
if exist "cppos.bin" (
    set "KERNEL=cppos.bin"
    goto :kernel_found
)

:: Kernel not found
:kernel_not_found
echo.
echo [ERROR] Kernel not found!
echo.
echo Searched locations:
echo   - %SCRIPT_DIR%releases\cppos.bin
if exist "%SCRIPT_DIR%releases" (echo     [DIR EXISTS]) else (echo     [DIR NOT FOUND])
echo   - %SCRIPT_DIR%build\cppos.bin
if exist "%SCRIPT_DIR%build" (echo     [DIR EXISTS]) else (echo     [DIR NOT FOUND])
echo   - releases\cppos.bin
if exist "releases" (echo     [DIR EXISTS]) else (echo     [DIR NOT FOUND])
echo   - build\cppos.bin
if exist "build" (echo     [DIR EXISTS]) else (echo     [DIR NOT FOUND])
echo   - cppos.bin (current dir)
echo.
echo The kernel needs to be built first!
echo.
echo Build options:
echo   1. MSYS2/MinGW: make
echo   2. WSL2: cd /mnt/c/.../CppOS ^&^& make
echo   3. GitHub Actions: See HOW_TO_BUILD.md
echo.
echo Or download pre-built binary from:
echo   https://github.com/YOUR_USERNAME/CppOS/releases
echo.
pause
exit /b 1

:kernel_found
echo [OK] Kernel: %KERNEL%
echo.
echo [OK] Starting CppOS...
echo    Press Ctrl+A then X in QEMU to exit
echo.

"%QEMU_CMD%" -kernel "%KERNEL%" -serial stdio
