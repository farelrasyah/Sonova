@echo off
title Quality Test - Enhanced YouTube Downloader

echo.
echo ========================================
echo  YouTube Video Quality Diagnostic
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if server is running
echo 🔍 Checking server status...
curl -s http://localhost:5000 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Server is not running on http://localhost:5000
    echo Please start the server first: start_enhanced_server.bat
    pause
    exit /b 1
)

echo ✅ Server is running
echo.

REM Get URL from user
set /p VIDEO_URL="Enter YouTube URL: "

if "%VIDEO_URL%"=="" (
    echo ❌ No URL provided
    pause
    exit /b 1
)

echo.
echo 🧪 Running quality analysis...
echo ========================================
python quick_quality_test.py "%VIDEO_URL%"

echo.
echo ========================================
echo 🔍 Detailed Analysis (Optional)
echo ========================================
set /p DETAILED="Run detailed analysis? (y/n): "

if /i "%DETAILED%"=="y" (
    echo.
    echo Running detailed quality analyzer...
    python quality_analyzer.py "%VIDEO_URL%"
)

echo.
echo ========================================
echo 🧪 Quality Verification Test (Optional)
echo ========================================
set /p VERIFY="Run download quality verification? (y/n): "

if /i "%VERIFY%"=="y" (
    echo.
    echo ⚠️  This will download test videos to verify quality
    echo Make sure you have enough disk space and good internet
    set /p CONFIRM="Continue? (y/n): "
    
    if /i "!CONFIRM!"=="y" (
        python test_quality_verification.py
    )
)

echo.
echo ========================================
echo 💡 Next Steps
echo ========================================
echo.
echo 1. Use the enhanced frontend: enhanced_frontend.html
echo 2. Try the best quality download endpoint
echo 3. Use specific format_id for maximum control
echo.
echo API Examples:
echo - Basic info: curl -X POST http://localhost:5000/info -d "url=%VIDEO_URL%"
echo - All formats: curl -X POST http://localhost:5000/formats -d "url=%VIDEO_URL%"
echo - Best quality: curl -X POST http://localhost:5000/download-best -d "url=%VIDEO_URL%" -d "format=mp4" -d "target_resolution=1080p" --output video.mp4
echo.

pause
