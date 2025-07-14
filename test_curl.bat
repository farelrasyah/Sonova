@echo off
REM Testing script untuk YouTube Downloader API menggunakan curl

echo 🚀 YouTube Downloader API Test Script
echo ========================================

REM Check if curl is available
curl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ curl not found. Please install curl or use Python test script.
    echo    Download curl from: https://curl.se/download.html
    pause
    exit /b 1
)

echo ✅ curl found

REM Test API connection
echo.
echo 🔍 Testing API connection...
curl -s -X GET http://localhost:5000/ | findstr "status"
if %errorlevel% neq 0 (
    echo ❌ API not responding. Make sure it's running on port 5000
    pause
    exit /b 1
)

echo ✅ API is running

REM Test video info
echo.
echo 📋 Testing video info...
curl -s -X POST ^
  -F "url=https://www.youtube.com/watch?v=jNQXAC9IVRw" ^
  http://localhost:5000/info > temp_info.json

findstr "error" temp_info.json >nul
if %errorlevel% equ 0 (
    echo ❌ Error getting video info:
    type temp_info.json
) else (
    echo ✅ Video info retrieved successfully
    findstr "title" temp_info.json
)

REM Test MP3 download
echo.
echo 🎵 Testing MP3 download...
echo    This may take a while...
curl -X POST ^
  -F "url=https://www.youtube.com/watch?v=jNQXAC9IVRw" ^
  -F "format=mp3" ^
  -o "test_download.mp3" ^
  http://localhost:5000/download

if exist "test_download.mp3" (
    for %%A in ("test_download.mp3") do (
        echo ✅ MP3 download successful: %%~zA bytes
    )
    del "test_download.mp3"
) else (
    echo ❌ MP3 download failed
)

REM Test MP4 download
echo.
echo 🎬 Testing MP4 download...
echo    This may take a while...
curl -X POST ^
  -F "url=https://www.youtube.com/watch?v=jNQXAC9IVRw" ^
  -F "format=mp4" ^
  -F "resolution=360p" ^
  -o "test_download.mp4" ^
  http://localhost:5000/download

if exist "test_download.mp4" (
    for %%A in ("test_download.mp4") do (
        echo ✅ MP4 download successful: %%~zA bytes
    )
    del "test_download.mp4"
) else (
    echo ❌ MP4 download failed
)

REM Cleanup
if exist "temp_info.json" del "temp_info.json"

echo.
echo 🏁 Testing completed!
echo    Check app.log for detailed logs
pause
