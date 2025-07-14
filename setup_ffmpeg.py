#!/usr/bin/env python3
"""
Check and setup ffmpeg for YouTube Downloader API
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ ffmpeg is already installed and working")
            return True
        else:
            print("❌ ffmpeg found but not working properly")
            return False
    except FileNotFoundError:
        print("❌ ffmpeg not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ ffmpeg check timed out")
        return False

def download_ffmpeg_windows():
    """Download and setup ffmpeg for Windows"""
    print("🔄 Downloading ffmpeg for Windows...")
    
    # Create ffmpeg directory
    ffmpeg_dir = os.path.join(os.getcwd(), 'ffmpeg')
    os.makedirs(ffmpeg_dir, exist_ok=True)
    
    # Download ffmpeg (using a smaller essential build)
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = os.path.join(ffmpeg_dir, 'ffmpeg.zip')
    
    try:
        print("📥 Downloading ffmpeg archive...")
        urllib.request.urlretrieve(ffmpeg_url, zip_path)
        
        print("📂 Extracting ffmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        # Find the extracted folder
        for item in os.listdir(ffmpeg_dir):
            item_path = os.path.join(ffmpeg_dir, item)
            if os.path.isdir(item_path) and 'ffmpeg' in item:
                # Move ffmpeg.exe to the main ffmpeg directory
                ffmpeg_exe = os.path.join(item_path, 'bin', 'ffmpeg.exe')
                if os.path.exists(ffmpeg_exe):
                    shutil.copy2(ffmpeg_exe, os.path.join(ffmpeg_dir, 'ffmpeg.exe'))
                    print(f"✅ ffmpeg.exe copied to {ffmpeg_dir}")
                    break
        
        # Cleanup
        os.remove(zip_path)
        
        # Add to PATH for current session
        ffmpeg_path = os.path.abspath(ffmpeg_dir)
        current_path = os.environ.get('PATH', '')
        if ffmpeg_path not in current_path:
            os.environ['PATH'] = ffmpeg_path + os.pathsep + current_path
            print(f"✅ Added {ffmpeg_path} to PATH for current session")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading ffmpeg: {e}")
        return False

def setup_ffmpeg():
    """Setup ffmpeg based on the operating system"""
    system = platform.system()
    
    if system == "Windows":
        if not check_ffmpeg():
            print("🔧 Setting up ffmpeg for Windows...")
            return download_ffmpeg_windows()
        return True
    
    elif system == "Darwin":  # macOS
        print("📝 For macOS, please install ffmpeg using Homebrew:")
        print("   brew install ffmpeg")
        return False
        
    else:  # Linux
        print("📝 For Linux, please install ffmpeg using your package manager:")
        print("   Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("   CentOS/RHEL: sudo yum install ffmpeg")
        print("   Fedora: sudo dnf install ffmpeg")
        return False

def test_ffmpeg_with_ytdlp():
    """Test if ffmpeg works with yt-dlp"""
    print("🧪 Testing ffmpeg with yt-dlp...")
    
    try:
        import yt_dlp
        
        # Test with a very short video
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll
        
        ydl_opts = {
            'format': 'worst[ext=mp4]',  # Use worst quality for faster test
            'outtmpl': 'test_video.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Just extract info to test if everything works
            info = ydl.extract_info(test_url, download=False)
            if info:
                print("✅ yt-dlp can extract video information")
                print(f"   Title: {info.get('title', 'Unknown')}")
                print(f"   Duration: {info.get('duration', 0)} seconds")
                return True
            else:
                print("❌ yt-dlp failed to extract video information")
                return False
                
    except ImportError:
        print("❌ yt-dlp not installed")
        return False
    except Exception as e:
        print(f"❌ Error testing yt-dlp: {e}")
        return False

def main():
    """Main function"""
    print("🔧 FFmpeg Setup for YouTube Downloader API")
    print("=" * 50)
    
    # Check current ffmpeg status
    if check_ffmpeg():
        print("✅ ffmpeg is ready!")
    else:
        print("⚠️  ffmpeg not found, attempting to set up...")
        if not setup_ffmpeg():
            print("❌ Failed to setup ffmpeg automatically")
            print("📝 Please install ffmpeg manually and add it to your PATH")
            return False
    
    # Test with yt-dlp
    if test_ffmpeg_with_ytdlp():
        print("\n🎉 Everything is ready!")
        print("✅ ffmpeg is installed and working")
        print("✅ yt-dlp can extract video information")
        print("\n🚀 You can now run your YouTube Downloader API!")
        return True
    else:
        print("\n❌ Setup incomplete")
        print("📝 Please check your ffmpeg and yt-dlp installation")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
