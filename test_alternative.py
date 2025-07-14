#!/usr/bin/env python3
"""
YouTube Downloader API - Alternative Test
Menggunakan video yang lebih aman untuk testing
"""

import requests
import json
import os
import time

API_BASE_URL = "http://localhost:5000"

# Video alternatif yang biasanya lebih stabil untuk testing
TEST_VIDEOS = [
    {
        "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo - video YouTube pertama
        "title": "Me at the zoo"
    },
    {
        "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Despacito
        "title": "Despacito"
    },
    {
        "url": "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Gangnam Style
        "title": "Gangnam Style"
    }
]

def test_api_connection():
    """Test koneksi API"""
    print("🔍 Testing API connection...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API connected successfully")
            print(f"   Version: {data.get('version')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ API responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        print("   Make sure the API is running: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_video_info(video_url, video_title):
    """Test video info endpoint"""
    print(f"\n📋 Testing video info for: {video_title}")
    try:
        response = requests.post(
            f"{API_BASE_URL}/info",
            data={"url": video_url},
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            info = response.json()
            print(f"   ✅ Title: {info.get('title', 'N/A')}")
            print(f"   ⏱️  Duration: {info.get('duration', 0)} seconds")
            print(f"   👤 Uploader: {info.get('uploader', 'N/A')}")
            formats = info.get('available_formats', [])
            if formats:
                print(f"   🎥 Available formats: {len(formats)}")
                for fmt in formats[:3]:  # Show first 3 formats
                    print(f"      - {fmt.get('resolution')} ({fmt.get('ext')})")
            return True
        else:
            error_data = response.json()
            print(f"   ❌ Error: {error_data.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Request timeout")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_mp3_download(video_url, video_title):
    """Test MP3 download"""
    print(f"\n🎵 Testing MP3 download for: {video_title}")
    try:
        response = requests.post(
            f"{API_BASE_URL}/download",
            data={
                "url": video_url,
                "format": "mp3"
            },
            timeout=120,  # 2 minutes timeout
            stream=True
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            # Get filename from headers
            content_disposition = response.headers.get('Content-Disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"')
            else:
                filename = f"test_audio_{int(time.time())}.mp3"
            
            # Save file
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(filename)
            print(f"   ✅ Download successful: {filename}")
            print(f"   📁 File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
            # Cleanup
            os.remove(filename)
            print(f"   🗑️  Cleaned up test file")
            return True
        else:
            try:
                error_data = response.json()
                print(f"   ❌ Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   ❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Download timeout (>2 minutes)")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_mp4_download(video_url, video_title):
    """Test MP4 download"""
    print(f"\n🎬 Testing MP4 download for: {video_title}")
    try:
        response = requests.post(
            f"{API_BASE_URL}/download",
            data={
                "url": video_url,
                "format": "mp4",
                "resolution": "360p"
            },
            timeout=180,  # 3 minutes timeout
            stream=True
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            # Get filename from headers
            content_disposition = response.headers.get('Content-Disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"')
            else:
                filename = f"test_video_{int(time.time())}.mp4"
            
            # Save file
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(filename)
            print(f"   ✅ Download successful: {filename}")
            print(f"   📁 File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
            # Cleanup
            os.remove(filename)
            print(f"   🗑️  Cleaned up test file")
            return True
        else:
            try:
                error_data = response.json()
                print(f"   ❌ Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   ❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Download timeout (>3 minutes)")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run comprehensive tests"""
    print("🚀 YouTube Downloader API - Comprehensive Test")
    print("=" * 60)
    
    # Test API connection first
    if not test_api_connection():
        print("\n❌ Cannot proceed without API connection")
        return
    
    print(f"\n🧪 Testing with {len(TEST_VIDEOS)} different videos")
    print("=" * 60)
    
    results = {
        'info': 0,
        'mp3': 0,
        'mp4': 0,
        'total': len(TEST_VIDEOS)
    }
    
    for i, video in enumerate(TEST_VIDEOS, 1):
        print(f"\n📹 TEST VIDEO {i}/{len(TEST_VIDEOS)}: {video['title']}")
        print("-" * 40)
        
        # Test info
        if test_video_info(video['url'], video['title']):
            results['info'] += 1
            
            # If info works, try downloads
            time.sleep(2)  # Wait between requests
            
            if test_mp3_download(video['url'], video['title']):
                results['mp3'] += 1
            
            time.sleep(2)  # Wait between requests
            
            if test_mp4_download(video['url'], video['title']):
                results['mp4'] += 1
        
        # Wait between videos to avoid rate limiting
        if i < len(TEST_VIDEOS):
            print(f"\n⏳ Waiting 5 seconds before next video...")
            time.sleep(5)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Video Info:   {results['info']}/{results['total']} ✅")
    print(f"MP3 Download: {results['mp3']}/{results['total']} ✅")
    print(f"MP4 Download: {results['mp4']}/{results['total']} ✅")
    
    total_tests = results['info'] + results['mp3'] + results['mp4']
    max_tests = results['total'] * 3
    success_rate = (total_tests / max_tests) * 100
    
    print(f"\nOverall Success Rate: {success_rate:.1f}% ({total_tests}/{max_tests})")
    
    if success_rate >= 80:
        print("🎉 API working well!")
    elif success_rate >= 50:
        print("⚠️  API partially working - check logs")
    else:
        print("❌ API needs troubleshooting")
    
    print("\n💡 Tips:")
    print("   - If downloads fail, try different videos")
    print("   - YouTube may block requests if too frequent")
    print("   - Check app.log for detailed error messages")

if __name__ == "__main__":
    main()
