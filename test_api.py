#!/usr/bin/env python3
"""
Test script untuk YouTube Downloader API
"""

import requests
import json
import os

API_BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_video_info():
    """Test video info endpoint"""
    print("\n🔍 Testing video info...")
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll untuk testing
    
    try:
        response = requests.post(f"{API_BASE_URL}/info", data={"url": test_url})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            info = response.json()
            print(f"Title: {info.get('title')}")
            print(f"Duration: {info.get('duration')} seconds")
            print(f"Uploader: {info.get('uploader')}")
            print(f"Available formats: {len(info.get('available_formats', []))}")
        else:
            print(f"Error: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mp3_download():
    """Test MP3 download"""
    print("\n🔍 Testing MP3 download...")
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/download",
            data={
                "url": test_url,
                "format": "mp3"
            },
            stream=True
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            filename = "test_audio.mp3"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(filename)
            print(f"✅ Downloaded: {filename} ({file_size} bytes)")
            
            # Cleanup
            os.remove(filename)
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mp4_download():
    """Test MP4 download"""
    print("\n🔍 Testing MP4 download...")
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/download",
            data={
                "url": test_url,
                "format": "mp4",
                "resolution": "360p"
            },
            stream=True
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            filename = "test_video.mp4"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(filename)
            print(f"✅ Downloaded: {filename} ({file_size} bytes)")
            
            # Cleanup
            os.remove(filename)
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n🔍 Testing error handling...")
    
    # Test invalid URL
    response = requests.post(
        f"{API_BASE_URL}/download",
        data={
            "url": "https://invalid-url.com",
            "format": "mp3"
        }
    )
    
    print(f"Invalid URL status: {response.status_code}")
    if response.status_code == 400:
        print("✅ Invalid URL properly rejected")
    
    # Test missing parameters
    response = requests.post(f"{API_BASE_URL}/download", data={})
    print(f"Missing params status: {response.status_code}")
    if response.status_code == 400:
        print("✅ Missing parameters properly rejected")
    
    return True

def main():
    """Run all tests"""
    print("🚀 YouTube Downloader API Test Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Video Info", test_video_info),
        ("MP3 Download", test_mp3_download),
        ("MP4 Download", test_mp4_download),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'=' * 20} {test_name} {'=' * 20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()
