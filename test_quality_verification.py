#!/usr/bin/env python3
"""
Quality Verification Test
Tes untuk memverifikasi bahwa video yang didownload benar-benar berkualitas HD
"""

import requests
import json
import os
import subprocess
import time
from urllib.parse import urlparse

def get_video_info_ffprobe(video_path):
    """Get video info using ffprobe"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams',
            '-show_format', video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def analyze_downloaded_quality(video_path):
    """Analyze the actual quality of downloaded video"""
    if not os.path.exists(video_path):
        return None
    
    info = get_video_info_ffprobe(video_path)
    if not info:
        return None
    
    video_stream = None
    audio_stream = None
    
    for stream in info.get('streams', []):
        if stream.get('codec_type') == 'video' and not video_stream:
            video_stream = stream
        elif stream.get('codec_type') == 'audio' and not audio_stream:
            audio_stream = stream
    
    result = {
        'file_size': os.path.getsize(video_path),
        'format': info.get('format', {}),
        'video_stream': video_stream,
        'audio_stream': audio_stream
    }
    
    return result

def test_quality_consistency():
    """Test if downloaded videos maintain promised quality"""
    
    base_url = "http://localhost:5000"
    test_videos = [
        {
            "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
            "title": "Me at the zoo (First YouTube video)"
        },
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
            "title": "Never Gonna Give You Up"
        }
    ]
    
    print("🧪 Quality Verification Test")
    print("=" * 50)
    print("Testing if downloaded videos match expected quality...")
    print()
    
    for video in test_videos:
        print(f"📹 Testing: {video['title']}")
        print(f"URL: {video['url']}")
        print("-" * 40)
        
        # Step 1: Get available formats
        try:
            response = requests.post(f"{base_url}/formats", data={"url": video["url"]})
            if response.status_code != 200:
                print("❌ Failed to get formats")
                continue
            
            formats_data = response.json()
            video_formats = formats_data.get('video_formats', [])
            
            if not video_formats:
                print("❌ No video formats available")
                continue
            
            # Test different quality levels
            test_resolutions = ['1080p', '720p', '480p']
            available_resolutions = [fmt.get('resolution') for fmt in video_formats]
            
            for target_resolution in test_resolutions:
                if target_resolution not in available_resolutions:
                    print(f"⏭️  {target_resolution}: Not available")
                    continue
                
                print(f"\n🎯 Testing {target_resolution} quality...")
                
                # Find expected format info
                expected_format = None
                for fmt in video_formats:
                    if fmt.get('resolution') == target_resolution:
                        expected_format = fmt
                        break
                
                if not expected_format:
                    print(f"❌ {target_resolution}: Expected format not found")
                    continue
                
                expected_height = expected_format.get('height')
                expected_bitrate = expected_format.get('tbr')
                expected_codec = expected_format.get('vcodec')
                
                print(f"   📋 Expected: {expected_height}p, {expected_bitrate} kbps, {expected_codec}")
                
                # Download using best quality endpoint
                download_data = {
                    "url": video["url"],
                    "format": "mp4",
                    "target_resolution": target_resolution
                }
                
                try:
                    start_time = time.time()
                    response = requests.post(f"{base_url}/download-best", data=download_data, stream=True)
                    
                    if response.status_code != 200:
                        print(f"   ❌ Download failed: {response.status_code}")
                        continue
                    
                    # Save file temporarily
                    test_filename = f"test_{target_resolution}_{int(time.time())}.mp4"
                    test_path = os.path.join("./test_downloads", test_filename)
                    os.makedirs("./test_downloads", exist_ok=True)
                    
                    with open(test_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    download_time = time.time() - start_time
                    
                    # Analyze actual quality
                    actual_info = analyze_downloaded_quality(test_path)
                    
                    if actual_info:
                        video_stream = actual_info['video_stream']
                        audio_stream = actual_info['audio_stream']
                        file_size = actual_info['file_size']
                        
                        actual_height = int(video_stream.get('height', 0))
                        actual_width = int(video_stream.get('width', 0))
                        actual_bitrate = int(video_stream.get('bit_rate', 0)) // 1000 if video_stream.get('bit_rate') else 0
                        actual_codec = video_stream.get('codec_name', 'Unknown')
                        actual_fps = eval(video_stream.get('r_frame_rate', '0/1')) if video_stream.get('r_frame_rate') else 0
                        
                        audio_bitrate = int(audio_stream.get('bit_rate', 0)) // 1000 if audio_stream and audio_stream.get('bit_rate') else 0
                        audio_codec = audio_stream.get('codec_name', 'Unknown') if audio_stream else 'None'
                        
                        print(f"   ✅ Downloaded: {actual_width}x{actual_height}, {actual_bitrate} kbps, {actual_codec}")
                        print(f"   📊 File size: {file_size / (1024*1024):.1f} MB")
                        print(f"   ⏱️  Download time: {download_time:.1f}s")
                        print(f"   🎵 Audio: {audio_bitrate} kbps {audio_codec}")
                        print(f"   🎬 FPS: {actual_fps:.1f}")
                        
                        # Quality verification
                        quality_issues = []
                        
                        # Check height
                        if actual_height < expected_height * 0.9:  # Allow 10% tolerance
                            quality_issues.append(f"Height too low: {actual_height} vs expected {expected_height}")
                        
                        # Check if it's actually HD
                        if target_resolution in ['1080p', '720p']:
                            if actual_height < 720:
                                quality_issues.append(f"Not HD quality: {actual_height}p is below HD standard")
                        
                        # Check codec quality
                        if 'h264' not in actual_codec.lower() and 'avc' not in actual_codec.lower():
                            quality_issues.append(f"Suboptimal codec: {actual_codec}")
                        
                        # Check file size (very small files might indicate poor quality)
                        min_size_mb = expected_height * 0.1  # Rough estimate: 0.1MB per vertical pixel
                        if file_size / (1024*1024) < min_size_mb:
                            quality_issues.append(f"File size suspiciously small: {file_size / (1024*1024):.1f} MB")
                        
                        if quality_issues:
                            print(f"   ⚠️  Quality Issues:")
                            for issue in quality_issues:
                                print(f"      • {issue}")
                        else:
                            print(f"   ✅ Quality verification PASSED")
                        
                    else:
                        print(f"   ❌ Could not analyze video quality (ffprobe failed)")
                    
                    # Cleanup
                    try:
                        os.remove(test_path)
                    except:
                        pass
                        
                except Exception as e:
                    print(f"   ❌ Download error: {e}")
                
                time.sleep(1)  # Small delay between tests
            
        except Exception as e:
            print(f"❌ Error testing {video['title']}: {e}")
        
        print(f"\n{'='*50}")
        time.sleep(2)

def test_format_id_accuracy():
    """Test if using specific format_id gives expected quality"""
    
    base_url = "http://localhost:5000"
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    print("\n🎯 Format ID Accuracy Test")
    print("=" * 50)
    
    # Get formats
    response = requests.post(f"{base_url}/formats", data={"url": test_url})
    if response.status_code != 200:
        print("❌ Failed to get formats")
        return
    
    formats_data = response.json()
    video_formats = formats_data.get('video_formats', [])
    
    if not video_formats:
        print("❌ No video formats available")
        return
    
    # Test the highest quality format
    best_format = max(video_formats, key=lambda x: x.get('tbr', 0) or 0)
    
    print(f"🎬 Testing highest quality format:")
    print(f"   Format ID: {best_format.get('format_id')}")
    print(f"   Resolution: {best_format.get('resolution')}")
    print(f"   Bitrate: {best_format.get('tbr')} kbps")
    print(f"   Codec: {best_format.get('vcodec')}")
    
    # Download with specific format ID
    download_data = {
        "url": test_url,
        "format": "mp4",
        "format_id": best_format.get('format_id')
    }
    
    try:
        response = requests.post(f"{base_url}/download", data=download_data, stream=True)
        
        if response.status_code != 200:
            print(f"❌ Download failed: {response.status_code}")
            return
        
        # Save and analyze
        test_filename = f"format_id_test_{int(time.time())}.mp4"
        test_path = os.path.join("./test_downloads", test_filename)
        os.makedirs("./test_downloads", exist_ok=True)
        
        with open(test_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        actual_info = analyze_downloaded_quality(test_path)
        
        if actual_info:
            video_stream = actual_info['video_stream']
            actual_height = int(video_stream.get('height', 0))
            actual_bitrate = int(video_stream.get('bit_rate', 0)) // 1000 if video_stream.get('bit_rate') else 0
            
            expected_height = best_format.get('height')
            expected_bitrate = best_format.get('tbr', 0)
            
            print(f"\n📊 Results:")
            print(f"   Expected: {expected_height}p @ {expected_bitrate} kbps")
            print(f"   Actual:   {actual_height}p @ {actual_bitrate} kbps")
            
            if actual_height == expected_height:
                print("   ✅ Resolution matches exactly")
            elif actual_height >= expected_height * 0.9:
                print("   ✅ Resolution within acceptable range")
            else:
                print("   ❌ Resolution significantly lower than expected")
            
            if abs(actual_bitrate - expected_bitrate) <= expected_bitrate * 0.2:
                print("   ✅ Bitrate within acceptable range")
            else:
                print("   ⚠️  Bitrate differs from expected")
        
        # Cleanup
        try:
            os.remove(test_path)
        except:
            pass
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Quality Verification Tests")
    print("Make sure the enhanced server is running on http://localhost:5000")
    print("Make sure ffprobe is installed for quality analysis")
    print()
    
    # Check if ffprobe is available
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        print("✅ ffprobe found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ffprobe not found. Quality analysis will be limited.")
        print("   Install ffmpeg to get detailed quality verification.")
    
    try:
        # Test if server is running
        response = requests.get("http://localhost:5000")
        if response.status_code == 200:
            print("✅ Server is running")
            test_quality_consistency()
            test_format_id_accuracy()
        else:
            print("❌ Server is not responding correctly")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n🏁 Quality verification tests completed!")
