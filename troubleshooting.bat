@echo off
echo ====================================
echo  YouTube Downloader Troubleshooting
echo ====================================
echo.

echo [1] Running full diagnostic...
python troubleshooting.py

echo.
echo [2] Press any key to test individual components...
pause > nul

:menu
cls
echo ====================================
echo  YouTube Downloader Troubleshooting
echo ====================================
echo.
echo Select test to run:
echo [1] API Connection Test
echo [2] FFmpeg Test
echo [3] YouTube Access Test
echo [4] Download Process Test
echo [5] Temp Directory Test
echo [6] Full Diagnostic
echo [7] Exit
echo.
set /p choice=Enter your choice (1-7): 

if "%choice%"=="1" (
    python troubleshooting.py api
    goto continue
)
if "%choice%"=="2" (
    python troubleshooting.py ffmpeg
    goto continue
)
if "%choice%"=="3" (
    python troubleshooting.py youtube
    goto continue
)
if "%choice%"=="4" (
    python troubleshooting.py download
    goto continue
)
if "%choice%"=="5" (
    python troubleshooting.py temp
    goto continue
)
if "%choice%"=="6" (
    python troubleshooting.py
    goto continue
)
if "%choice%"=="7" (
    exit
)

echo Invalid choice. Please try again.
goto continue

:continue
echo.
echo Press any key to return to menu...
pause > nul
goto menu
