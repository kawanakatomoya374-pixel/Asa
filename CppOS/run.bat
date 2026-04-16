@echo off
chcp 65001 >nul
title CppOS - Quick Launcher

:: Get script directory
cd /d "%~dp0"

echo ======================================
echo   CppOS - C++ Operating System
echo ======================================
echo.
echo Working directory: %CD%
echo.

:: Find QEMU
set "QEMU=qemu-system-i386"
where qemu-system-i386 >nul 2>&1
if %ERRORLEVEL% EQU 0 goto :qemu_ok

:: Try common paths
set "QEMU_PATHS=C:\Program Files\qemu\qemu-system-i386.exe;C:\Program Files (x86)\qemu\qemu-system-i386.exe;C:\msys64\mingw64\bin\qemu-system-i386.exe;C:\msys64\mingw32\bin\qemu-system-i386.exe;C:\msys64\usr\bin\qemu-system-i386.exe"
for %%Q in (%QEMU_PATHS%) do (
    if exist "%%Q" (
        set "QEMU=%%Q"
        goto :qemu_ok
    )
)

echo [ERROR] QEMU not found!
echo.
echo Please install QEMU from: https://qemu.weilnetz.de/w64/
echo Or use MSYS2: pacman -S qemu
echo.
pause
exit /b 1

:qemu_ok
echo [OK] QEMU: %QEMU%

:: Find kernel
set "KERNEL="
if exist "releases\cppos.bin" set "KERNEL=releases\cppos.bin"
if exist "build\cppos.bin" set "KERNEL=build\cppos.bin"
if exist "cppos.bin" set "KERNEL=cppos.bin"

if "%KERNEL%"=="" (
    echo.
    echo [ERROR] Kernel binary not found!
    echo.
    echo Searched: releases\cppos.bin, build\cppos.bin, cppos.bin
    echo.
    echo Please build the kernel first:
    echo   make
    echo.
    pause
    exit /b 1
)

echo [OK] Kernel: %KERNEL%
echo.
echo Starting CppOS...
echo.
"%QEMU%" -kernel "%KERNEL%" -serial stdio
