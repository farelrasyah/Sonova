#!/usr/bin/env python3
"""
Test Enhanced YouTube Downloader API
Test script untuk menguji fitur-fitur baru dengan berbagai kualitas video
"""

import requests
import json
import time
import os

def test_api():
    base_url = "http://localhost:5000"
    
    # Test URLs with different quality options
    test_videos = [
        {
            "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # First YouTube video (short)
            "title": "Me at the zoo"
        },
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll (popular)
            "title": "Rick Astley - Never Gonna Give You Up"
        }
    ]
    
    print("🧪 Testing Enhanced YouTube Downloader API")
    print("=" * 50)
    
    for video in test_videos:
        print(f"\n📹 Testing: {video['title']}")
        print(f"URL: {video['url']}")
        print("-" * 40)
        
        # Test 1: Get basic video info
        print("\n1️⃣ Testing basic video info...")
        try:
            response = requests.post(f"{base_url}/info", data={"url": video["url"]})
            if response.status_code == 200:
                info = response.json()
                print(f"✅ Title: {info.get('title', 'Unknown')}")
                print(f"✅ Duration: {info.get('duration', 0)} seconds")
                print(f"✅ Views: {info.get('view_count', 0):,}")
                print(f"✅ Available formats: {len(info.get('available_formats', []))}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test 2: Get detailed formats
        print("\n2️⃣ Testing detailed formats...")
        try:
            response = requests.post(f"{base_url}/formats", data={"url": video["url"]})
            if response.status_code == 200:
                formats = response.json()
                
                video_formats = formats.get('video_formats', [])
                audio_formats = formats.get('audio_formats', [])
                
                print(f"✅ Video formats found: {len(video_formats)}")
                if video_formats:
                    print("   Top 3 video qualities:")
                    for i, fmt in enumerate(video_formats[:3]):
                        bitrate = f"({fmt.get('tbr', 'Unknown')} kbps)" if fmt.get('tbr') else ""
                        size = f"~{fmt.get('filesize', 0) // (1024*1024) if fmt.get('filesize') else '?'} MB"
                        print(f"   • {fmt.get('resolution')} - {fmt.get('vcodec', 'Unknown')} {bitrate} {size}")
                
                print(f"✅ Audio formats found: {len(audio_formats)}")
                if audio_formats:
                    print("   Top 3 audio qualities:")
                    for i, fmt in enumerate(audio_formats[:3]):
                        size = f"~{fmt.get('filesize', 0) // (1024*1024) if fmt.get('filesize') else '?'} MB"
                        print(f"   • {fmt.get('quality')} - {fmt.get('acodec', 'Unknown')} {size}")
                
                # Test 3: Download highest quality video (if available)
                if video_formats:
                    print(f"\n3️⃣ Testing high-quality video download...")
                    highest_quality = video_formats[0]  # First one should be highest
                    
                    download_data = {
                        "url": video["url"],
                        "format": "mp4",
                        "resolution": highest_quality.get('resolution'),
                        "format_id": highest_quality.get('format_id')
                    }
                    
                    print(f"   Requesting: {highest_quality.get('resolution')} ({highest_quality.get('format_id')})")
                    
                    try:
                        response = requests.post(f"{base_url}/download", data=download_data, stream=True)
                        
                        if response.status_code == 200:
                            # Get filename from headers
                            content_disposition = response.headers.get('content-disposition', '')
                            if 'filename=' in content_disposition:
                                filename = content_disposition.split('filename=')[1].strip('"')
                            else:
                                filename = f"test_video_{int(time.time())}.mp4"
                            
                            # Save file
                            test_dir = "./test_downloads"
                            os.makedirs(test_dir, exist_ok=True)
                            filepath = os.path.join(test_dir, filename)
                            
                            with open(filepath, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            file_size = os.path.getsize(filepath)
                            print(f"   ✅ Downloaded: {filename}")
                            print(f"   ✅ File size: {file_size / (1024*1024):.1f} MB")
                            
                            # Clean up test file (optional)
                            # os.remove(filepath)
                            
                        else:
                            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                            print(f"   ❌ Download failed: {response.status_code} - {error_data}")
                    
                    except Exception as e:
                        print(f"   ❌ Download exception: {e}")
                
                # Test 4: Download highest quality audio
                if audio_formats:
                    print(f"\n4️⃣ Testing high-quality audio download...")
                    highest_audio = audio_formats[0]  # First one should be highest
                    
                    download_data = {
                        "url": video["url"],
                        "format": "mp3",
                        "audio_quality": str(int(highest_audio.get('abr', 320)))
                    }
                    
                    print(f"   Requesting: {highest_audio.get('quality')} ({highest_audio.get('abr')} kbps)")
                    
                    try:
                        response = requests.post(f"{base_url}/download", data=download_data, stream=True)
                        
                        if response.status_code == 200:
                            # Get filename from headers
                            content_disposition = response.headers.get('content-disposition', '')
                            if 'filename=' in content_disposition:
                                filename = content_disposition.split('filename=')[1].strip('"')
                            else:
                                filename = f"test_audio_{int(time.time())}.mp3"
                            
                            # Save file
                            test_dir = "./test_downloads"
                            os.makedirs(test_dir, exist_ok=True)
                            filepath = os.path.join(test_dir, filename)
                            
                            with open(filepath, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            file_size = os.path.getsize(filepath)
                            print(f"   ✅ Downloaded: {filename}")
                            print(f"   ✅ File size: {file_size / (1024*1024):.1f} MB")
                            
                            # Clean up test file (optional)
                            # os.remove(filepath)
                            
                        else:
                            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                            print(f"   ❌ Download failed: {response.status_code} - {error_data}")
                    
                    except Exception as e:
                        print(f"   ❌ Download exception: {e}")
                        
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print(f"\n{'='*50}")
        time.sleep(2)  # Wait between tests

def test_quality_comparison():
    """Test different quality settings for the same video"""
    base_url = "http://localhost:5000"
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # Short video for testing
    
    print("\n🔍 Quality Comparison Test")
    print("=" * 50)
    
    # Get available formats first
    response = requests.post(f"{base_url}/formats", data={"url": test_url})
    if response.status_code != 200:
        print("❌ Failed to get formats")
        return
    
    formats = response.json()
    video_formats = formats.get('video_formats', [])
    
    if not video_formats:
        print("❌ No video formats available")
        return
    
    print(f"📹 Available resolutions for quality testing:")
    for i, fmt in enumerate(video_formats):
        bitrate = f"({fmt.get('tbr', '?')} kbps)" if fmt.get('tbr') else ""
        print(f"   {i+1}. {fmt.get('resolution')} - {fmt.get('vcodec', 'Unknown')} {bitrate}")
    
    # Test different resolutions
    test_resolutions = ['1080p', '720p', '480p', '360p']
    available_resolutions = [fmt.get('resolution') for fmt in video_formats]
    
    print(f"\n🧪 Testing different resolutions...")
    
    for resolution in test_resolutions:
        if resolution in available_resolutions:
            print(f"\n📥 Testing {resolution}...")
            
            download_data = {
                "url": test_url,
                "format": "mp4",
                "resolution": resolution
            }
            
            try:
                start_time = time.time()
                response = requests.post(f"{base_url}/download", data=download_data, stream=True)
                
                if response.status_code == 200:
                    # Calculate download without actually saving
                    total_size = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        total_size += len(chunk)
                    
                    download_time = time.time() - start_time
                    
                    print(f"   ✅ {resolution}: {total_size / (1024*1024):.1f} MB in {download_time:.1f}s")
                else:
                    print(f"   ❌ {resolution}: Failed ({response.status_code})")
            
            except Exception as e:
                print(f"   ❌ {resolution}: Exception - {e}")
        else:
            print(f"   ⏭️ {resolution}: Not available")

if __name__ == "__main__":
    print("🚀 Starting Enhanced YouTube Downloader Tests")
    print("Make sure the server is running on http://localhost:5000")
    print()
    
    try:
        # Test if server is running
        response = requests.get("http://localhost:5000")
        if response.status_code == 200:
            print("✅ Server is running")
            test_api()
            test_quality_comparison()
        else:
            print("❌ Server is not responding correctly")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n🏁 Tests completed!")
