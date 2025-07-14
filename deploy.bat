@echo off
REM Production deployment script for Windows

echo 🚀 Starting YouTube Downloader API deployment...

REM Check if ffmpeg is installed
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ffmpeg not found. Please install ffmpeg first:
    echo    Download from https://ffmpeg.org/download.html
    echo    Add ffmpeg.exe to your PATH
    exit /b 1
)

REM Create necessary directories
if not exist "temp" mkdir temp
if not exist "logs" mkdir logs

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Set environment variables
set FLASK_ENV=production
set FLASK_DEBUG=False

REM Start the application
echo 🔥 Starting application...
python app.py

echo ✅ YouTube Downloader API started successfully!
