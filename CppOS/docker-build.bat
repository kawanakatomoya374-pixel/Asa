@echo off
chcp 65001 >nul
echo ======================================
echo   CppOS Docker Build
echo ======================================
echo.

:: Check Docker
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker not found!
    echo.
    echo Please install Docker Desktop:
    echo https://www.docker.com/products/docker-desktop
    echo.
    start https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [OK] Docker found
echo [INFO] Building CppOS using Docker...
echo.

:: Build using Docker
docker build -t cppos-builder .
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker build failed!
    pause
    exit /b 1
)

:: Run container to build
docker run --rm -v "%CD%:/cppos" cppos-builder make
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [OK] Build successful!
echo Kernel location: build\cppos.bin
pause
