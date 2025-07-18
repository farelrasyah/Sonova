#!/usr/bin/env python3
"""
Troubleshooting tool untuk YouTube Downloader
Digunakan untuk mendiagnosis masalah koneksi dan download
"""

import os
import sys
import time
import requests
import subprocess
from urllib.parse import urlparse
import yt_dlp
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TroubleshootingTool:
    def __init__(self):
        self.api_url = "http://localhost:5000"
        self.test_urls = [
            "https://youtu.be/jNQXAC9IVRw",  # Me at the zoo (first YouTube video)
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
        ]
    
    def test_api_connection(self):
        """Test API server connection"""
        print("=" * 50)
        print("🔍 Testing API Connection...")
        print("=" * 50)
        
        try:
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                print("✅ API server is running and accessible")
                data = response.json()
                print(f"📊 API Version: {data.get('version', 'Unknown')}")
                print(f"📊 API Status: {data.get('status', 'Unknown')}")
                return True
            else:
                print(f"❌ API server returned status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API server")
            print("💡 Make sure to run: python app.py")
            return False
        except Exception as e:
            print(f"❌ API connection error: {e}")
            return False
    
    def test_ffmpeg(self):
        """Test FFmpeg installation"""
        print("\n" + "=" * 50)
        print("🔍 Testing FFmpeg Installation...")
        print("=" * 50)
        
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ FFmpeg is installed and working")
                version_line = result.stdout.split('\n')[0]
                print(f"📊 {version_line}")
                return True
            else:
                print("❌ FFmpeg is not working properly")
                return False
        except FileNotFoundError:
            print("❌ FFmpeg is not installed or not in PATH")
            print("💡 Install FFmpeg or run: python setup_ffmpeg.py")
            return False
        except Exception as e:
            print(f"❌ FFmpeg test error: {e}")
            return False
    
    def test_youtube_access(self):
        """Test YouTube accessibility"""
        print("\n" + "=" * 50)
        print("🔍 Testing YouTube Access...")
        print("=" * 50)
        
        test_url = self.test_urls[0]
        print(f"📹 Testing URL: {test_url}")
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'retries': 3,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(test_url, download=False)
                if info:
                    print("✅ YouTube access is working")
                    print(f"📊 Video Title: {info.get('title', 'Unknown')}")
                    print(f"📊 Duration: {info.get('duration', 0)} seconds")
                    print(f"📊 Available formats: {len(info.get('formats', []))}")
                    return True
                else:
                    print("❌ Cannot extract video information")
                    return False
        except Exception as e:
            print(f"❌ YouTube access error: {e}")
            print("💡 This might indicate network issues or YouTube blocking")
            return False
    
    def test_download_process(self):
        """Test actual download process"""
        print("\n" + "=" * 50)
        print("🔍 Testing Download Process...")
        print("=" * 50)
        
        if not self.test_api_connection():
            print("❌ Skipping download test - API not accessible")
            return False
        
        test_url = self.test_urls[0]
        print(f"📹 Testing download with URL: {test_url}")
        
        try:
            # Test video info
            print("🔍 Step 1: Getting video info...")
            info_data = {'url': test_url}
            response = requests.post(f"{self.api_url}/info", data=info_data, timeout=30)
            
            if response.status_code == 200:
                info = response.json()
                print(f"✅ Video info retrieved: {info.get('title', 'Unknown')}")
            else:
                print(f"❌ Failed to get video info: {response.status_code}")
                return False
            
            # Test MP3 download
            print("🔍 Step 2: Testing MP3 download...")
            download_data = {'url': test_url, 'format': 'mp3'}
            response = requests.post(f"{self.api_url}/download", data=download_data, timeout=120)
            
            if response.status_code == 200:
                print("✅ MP3 download successful")
                print(f"📊 Content Type: {response.headers.get('content-type', 'Unknown')}")
                print(f"📊 Content Length: {len(response.content)} bytes")
            else:
                print(f"❌ MP3 download failed: {response.status_code}")
                if response.headers.get('content-type') == 'application/json':
                    error_data = response.json()
                    print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
                return False
            
            # Test MP4 download
            print("🔍 Step 3: Testing MP4 download...")
            download_data = {'url': test_url, 'format': 'mp4', 'resolution': '720p'}
            response = requests.post(f"{self.api_url}/download", data=download_data, timeout=180)
            
            if response.status_code == 200:
                print("✅ MP4 download successful")
                print(f"📊 Content Type: {response.headers.get('content-type', 'Unknown')}")
                print(f"📊 Content Length: {len(response.content)} bytes")
                return True
            else:
                print(f"❌ MP4 download failed: {response.status_code}")
                if response.headers.get('content-type') == 'application/json':
                    error_data = response.json()
                    print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Download test timed out")
            print("💡 This might indicate the download process is too slow")
            return False
        except Exception as e:
            print(f"❌ Download test error: {e}")
            return False
    
    def test_temp_directory(self):
        """Test temp directory permissions"""
        print("\n" + "=" * 50)
        print("🔍 Testing Temp Directory...")
        print("=" * 50)
        
        temp_dir = "./temp"
        
        try:
            # Check if temp directory exists
            if os.path.exists(temp_dir):
                print(f"✅ Temp directory exists: {temp_dir}")
            else:
                print(f"⚠️  Temp directory does not exist, creating: {temp_dir}")
                os.makedirs(temp_dir, exist_ok=True)
                print("✅ Temp directory created successfully")
            
            # Test write permission
            test_file = os.path.join(temp_dir, "test_write.txt")
            with open(test_file, 'w') as f:
                f.write("test")
            
            if os.path.exists(test_file):
                print("✅ Write permission test passed")
                os.remove(test_file)
                print("✅ File cleanup test passed")
                return True
            else:
                print("❌ Write permission test failed")
                return False
                
        except Exception as e:
            print(f"❌ Temp directory test error: {e}")
            return False
    
    def run_full_diagnostic(self):
        """Run full diagnostic test"""
        print("🚀 Starting Full Diagnostic...")
        print("=" * 50)
        
        tests = [
            ("API Connection", self.test_api_connection),
            ("FFmpeg Installation", self.test_ffmpeg),
            ("Temp Directory", self.test_temp_directory),
            ("YouTube Access", self.test_youtube_access),
            ("Download Process", self.test_download_process),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                if result:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results.append((test_name, False))
        
        print("\n" + "=" * 50)
        print("📋 DIAGNOSTIC SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        print(f"\n📊 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your system is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the issues above.")
            print("\n💡 Common solutions:")
            print("   - Make sure to run: python app.py")
            print("   - Install FFmpeg: python setup_ffmpeg.py")
            print("   - Check your internet connection")
            print("   - Try running as administrator")
        
        return passed == total

def main():
    """Main function"""
    tool = TroubleshootingTool()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'api':
            tool.test_api_connection()
        elif command == 'ffmpeg':
            tool.test_ffmpeg()
        elif command == 'youtube':
            tool.test_youtube_access()
        elif command == 'download':
            tool.test_download_process()
        elif command == 'temp':
            tool.test_temp_directory()
        else:
            print("Available commands: api, ffmpeg, youtube, download, temp")
    else:
        tool.run_full_diagnostic()

if __name__ == "__main__":
    main()
