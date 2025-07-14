@echo off
title Enhanced YouTube Downloader Server

echo.
echo ========================================
echo  Enhanced YouTube Downloader Server
echo  High Quality Video ^& Audio Downloads
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Check if required packages are installed
echo.
echo 📦 Checking dependencies...
python -c "import yt_dlp, flask, flask_cors" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Required packages not found. Installing...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo ✅ All dependencies found
)

REM Check if FFmpeg is available
echo.
echo 🎬 Checking FFmpeg...
if exist "ffmpeg\ffmpeg.exe" (
    echo ✅ FFmpeg found in local directory
    set PATH=%CD%\ffmpeg;%PATH%
) else (
    ffmpeg -version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️  FFmpeg not found. Some features may not work optimally.
        echo    You can download FFmpeg and place ffmpeg.exe in the ffmpeg folder
    ) else (
        echo ✅ FFmpeg found in system PATH
    )
)

REM Set environment variables for better performance
set FLASK_ENV=production
set FLASK_DEBUG=false
set MAX_CONTENT_LENGTH=1073741824

REM Create temp directory if it doesn't exist
if not exist "temp" mkdir temp

echo.
echo 🚀 Starting Enhanced YouTube Downloader Server...
echo.
echo Server will be available at:
echo   📱 Frontend: http://localhost:5000/enhanced_frontend.html  
echo   🔗 API:      http://localhost:5000
echo.
echo Available endpoints:
echo   GET  /           - API information
echo   POST /info       - Basic video information  
echo   POST /formats    - Detailed format information
echo   POST /download   - Download with quality options
echo.
echo 💡 Tips for best quality:
echo   1. Use /formats endpoint first to see available qualities
echo   2. Specify format_id for exact quality control
echo   3. Use resolution parameter for automatic quality selection
echo   4. Set audio_quality to 320 for best audio
echo.
echo Press Ctrl+C to stop the server
echo ========================================

REM Start the server
python app.py

echo.
echo 🛑 Server stopped
pause
