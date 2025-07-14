#!/usr/bin/env python3
"""
Quick Quality Test
Tes cepat untuk mengecek apakah video bisa download HD
"""

import requests
import sys

def quick_quality_test(url):
    """Quick test untuk cek kualitas tersedia"""
    
    base_url = "http://localhost:5000"
    
    print("🚀 Quick Quality Test")
    print("=" * 30)
    print(f"Testing: {url}")
    print()
    
    try:
        # Test server
        response = requests.get(base_url, timeout=5)
        if response.status_code != 200:
            print("❌ Server not responding")
            return False
        print("✅ Server OK")
        
        # Get formats
        response = requests.post(f"{base_url}/formats", data={"url": url}, timeout=30)
        if response.status_code != 200:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"❌ Failed to get formats: {error_data}")
            return False
        
        data = response.json()
        video_formats = data.get('video_formats', [])
        
        if not video_formats:
            print("❌ No video formats available")
            return False
        
        print(f"✅ Found {len(video_formats)} video formats")
        
        # Check HD availability
        hd_formats = [f for f in video_formats if f.get('height', 0) >= 720]
        fhd_formats = [f for f in video_formats if f.get('height', 0) >= 1080]
        uhd_formats = [f for f in video_formats if f.get('height', 0) >= 1440]
        
        print(f"📊 Quality Summary:")
        print(f"   HD (720p+):   {len(hd_formats)} formats")
        print(f"   FHD (1080p+): {len(fhd_formats)} formats") 
        print(f"   UHD (1440p+): {len(uhd_formats)} formats")
        
        if fhd_formats:
            best_fhd = max(fhd_formats, key=lambda x: x.get('tbr', 0))
            print(f"🏆 Best FHD: {best_fhd.get('resolution')} @ {best_fhd.get('tbr')} kbps")
            recommendation = "1080p"
        elif hd_formats:
            best_hd = max(hd_formats, key=lambda x: x.get('tbr', 0))
            print(f"🥇 Best HD: {best_hd.get('resolution')} @ {best_hd.get('tbr')} kbps")
            recommendation = "720p"
        else:
            best_overall = max(video_formats, key=lambda x: x.get('tbr', 0))
            print(f"📱 Best Available: {best_overall.get('resolution')} @ {best_overall.get('tbr')} kbps")
            recommendation = best_overall.get('resolution')
        
        # Quick download test (just headers, no actual download)
        print(f"\n🧪 Testing download capability...")
        test_data = {
            "url": url,
            "format": "mp4"
        }
        
        # Test best quality endpoint
        response = requests.post(f"{base_url}/download-best", data=test_data, stream=True)
        if response.status_code == 200:
            print("✅ Best quality download: Ready")
            
            # Check content length if available
            content_length = response.headers.get('content-length')
            if content_length:
                size_mb = int(content_length) / (1024 * 1024)
                print(f"📦 Estimated size: {size_mb:.1f} MB")
            
            # Close connection without downloading
            response.close()
        else:
            print(f"⚠️  Download test failed: {response.status_code}")
        
        print(f"\n💡 Recommendation:")
        print(f"   Use target_resolution: {recommendation}")
        print(f"   Command:")
        print(f"   curl -X POST {base_url}/download-best \\")
        print(f"     -d \"url={url}\" \\")
        print(f"     -d \"format=mp4\" \\")
        print(f"     -d \"target_resolution={recommendation}\" \\")
        print(f"     --output \"video.mp4\"")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("   Make sure server is running: python app.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timeout")
        print("   Server might be overloaded or video processing is slow")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_quality_test.py <youtube_url>")
        print("Example: python quick_quality_test.py 'https://www.youtube.com/watch?v=jNQXAC9IVRw'")
        sys.exit(1)
    
    url = sys.argv[1]
    success = quick_quality_test(url)
    sys.exit(0 if success else 1)
