@echo off
echo ===================================================
echo    Titan Headless Enhanced - Windows Launcher
echo ===================================================
echo.

REM Set console colors for better visibility
color 0A

echo [INFO] Checking Node.js installation...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo [INFO] Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [INFO] Node.js found: 
node --version

echo.
echo [INFO] Checking for dependencies...
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    echo [INFO] This may take a few minutes on first run...
    npm install puppeteer-extra puppeteer-extra-plugin-stealth random-useragent proxy-chain faker axios
    if %ERRORLEVEL% NEQ 0 (
        echo [WARN] Standard install failed, trying with --force...
        npm install --force puppeteer-extra puppeteer-extra-plugin-stealth random-useragent proxy-chain faker axios
    )
) else (
    echo [INFO] Dependencies already present.
)

echo.
echo [INFO] Optimizing Windows environment...
REM Windows-specific optimizations handled by Node.js enhancements.js

echo.
echo [INFO] Starting Titan Headless Enhanced...
echo [INFO] Press Ctrl+C to stop the application
echo.

REM Set environment variables for Windows
set HEADLESS=true
set ENABLE_ENHANCEMENTS=true

REM Launch the application
node main.js

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application failed to start. Error code: %ERRORLEVEL%
    echo [INFO] Please check the error messages above.
    echo.
)

echo.
echo [INFO] Application finished.
pause