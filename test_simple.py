#!/usr/bin/env python3
"""
Simple YouTube Downloader Test Script
Contoh sederhana untuk testing API
"""

import requests
import json
import os
import time

# Konfigurasi API
API_BASE_URL = "http://localhost:5000"

def test_download_mp3():
    """Test download MP3 dengan contoh video pendek"""
    print("\n🎵 Testing MP3 Download...")
    
    # Gunakan video pendek untuk testing (contoh: video musik 30 detik)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - video klasik untuk testing
    
    try:
        # Kirim request download
        response = requests.post(
            f"{API_BASE_URL}/download",
            data={
                "url": test_url,
                "format": "mp3"
            },
            stream=True,
            timeout=300  # 5 menit timeout
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Ambil nama file dari header
            content_disposition = response.headers.get('Content-Disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"')
            else:
                filename = "downloaded_audio.mp3"
            
            # Simpan file
            print(f"📥 Downloading: {filename}")
            file_size = 0
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        file_size += len(chunk)
            
            print(f"✅ Download berhasil!")
            print(f"📁 File: {filename}")
            print(f"📊 Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
            return True
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            print(f"❌ Error: {error_data}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - download memakan waktu terlalu lama")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_download_mp4():
    """Test download MP4 dengan resolusi tertentu"""
    print("\n🎬 Testing MP4 Download...")
    
    # Gunakan video pendek untuk testing
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        # Kirim request download
        response = requests.post(
            f"{API_BASE_URL}/download",
            data={
                "url": test_url,
                "format": "mp4",
                "resolution": "360p"  # Pilih resolusi rendah untuk testing cepat
            },
            stream=True,
            timeout=300
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Ambil nama file dari header
            content_disposition = response.headers.get('Content-Disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"')
            else:
                filename = "downloaded_video.mp4"
            
            # Simpan file
            print(f"📥 Downloading: {filename}")
            file_size = 0
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        file_size += len(chunk)
            
            print(f"✅ Download berhasil!")
            print(f"📁 File: {filename}")
            print(f"📊 Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
            return True
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            print(f"❌ Error: {error_data}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - download memakan waktu terlalu lama")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_video_info():
    """Test mendapatkan info video"""
    print("\n📋 Testing Video Info...")
    
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/info",
            data={"url": test_url},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            info = response.json()
            print("✅ Info berhasil diambil:")
            print(f"📺 Title: {info.get('title', 'N/A')}")
            print(f"⏱️  Duration: {info.get('duration', 0)} seconds")
            print(f"👤 Uploader: {info.get('uploader', 'N/A')}")
            print(f"👁️  Views: {info.get('view_count', 0):,}")
            
            formats = info.get('available_formats', [])
            if formats:
                print("🎥 Available resolutions:")
                for fmt in formats[:5]:  # Show first 5 formats
                    print(f"   - {fmt.get('resolution', 'N/A')} ({fmt.get('ext', 'N/A')})")
            
            return True
        else:
            error_data = response.json()
            print(f"❌ Error: {error_data}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_with_custom_url():
    """Test dengan URL yang diinput user"""
    print("\n🔗 Custom URL Test")
    print("Masukkan URL YouTube yang ingin ditest:")
    print("(atau tekan Enter untuk skip)")
    
    custom_url = input("URL: ").strip()
    
    if not custom_url:
        print("Skipped custom URL test")
        return True
    
    # Test info dulu
    print(f"\n📋 Getting info for: {custom_url}")
    try:
        response = requests.post(
            f"{API_BASE_URL}/info",
            data={"url": custom_url},
            timeout=30
        )
        
        if response.status_code == 200:
            info = response.json()
            print(f"✅ Title: {info.get('title', 'N/A')}")
            print(f"⏱️  Duration: {info.get('duration', 0)} seconds")
            
            # Tanya user mau download format apa
            print("\nPilih format download:")
            print("1. MP3 (Audio only)")
            print("2. MP4 (Video)")
            print("3. Skip download")
            
            choice = input("Pilihan (1/2/3): ").strip()
            
            if choice == "1":
                print("\n🎵 Downloading MP3...")
                response = requests.post(
                    f"{API_BASE_URL}/download",
                    data={
                        "url": custom_url,
                        "format": "mp3"
                    },
                    stream=True,
                    timeout=300
                )
                
                if response.status_code == 200:
                    filename = f"custom_download_{int(time.time())}.mp3"
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    file_size = os.path.getsize(filename)
                    print(f"✅ MP3 Downloaded: {filename} ({file_size:,} bytes)")
                else:
                    print(f"❌ Download failed: {response.text}")
                    
            elif choice == "2":
                # Tanya resolusi
                print("\nPilih resolusi:")
                print("1. 360p (cepat)")
                print("2. 720p (medium)")
                print("3. 1080p (lambat)")
                
                res_choice = input("Pilihan (1/2/3): ").strip()
                resolution = {"1": "360p", "2": "720p", "3": "1080p"}.get(res_choice, "360p")
                
                print(f"\n🎬 Downloading MP4 ({resolution})...")
                response = requests.post(
                    f"{API_BASE_URL}/download",
                    data={
                        "url": custom_url,
                        "format": "mp4",
                        "resolution": resolution
                    },
                    stream=True,
                    timeout=300
                )
                
                if response.status_code == 200:
                    filename = f"custom_download_{int(time.time())}.mp4"
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    file_size = os.path.getsize(filename)
                    print(f"✅ MP4 Downloaded: {filename} ({file_size:,} bytes)")
                else:
                    print(f"❌ Download failed: {response.text}")
            
            return True
        else:
            print(f"❌ Failed to get video info: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main testing function"""
    print("🚀 YouTube Downloader API - Simple Test")
    print("=" * 50)
    
    # Check API availability
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ API is running")
            api_info = response.json()
            print(f"📍 API: {api_info.get('message', 'N/A')}")
            print(f"🔖 Version: {api_info.get('version', 'N/A')}")
        else:
            print("❌ API not responding properly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the API is running on http://localhost:5000")
        return
    
    print("\n" + "=" * 50)
    print("🧪 RUNNING TESTS")
    print("=" * 50)
    
    # Run tests
    tests = []
    
    # Test 1: Video Info
    tests.append(("Video Info", test_video_info()))
    
    # Test 2: MP3 Download
    tests.append(("MP3 Download", test_download_mp3()))
    
    # Test 3: MP4 Download
    tests.append(("MP4 Download", test_download_mp4()))
    
    # Test 4: Custom URL (optional)
    tests.append(("Custom URL", test_with_custom_url()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<15}: {status}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
    
    print("\n💡 Tips:")
    print("- File hasil download akan tersimpan di direktori saat ini")
    print("- Untuk testing dengan video yang lebih cepat, gunakan video pendek")
    print("- Jika download lambat, coba dengan resolusi yang lebih rendah")

if __name__ == "__main__":
    main()
