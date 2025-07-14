#!/usr/bin/env python3
"""
YouTube Video Quality Diagnostic Tool
Alat untuk menganalisis dan mendiagnosis kualitas video yang tersedia
"""

import requests
import json
import sys
import argparse
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    if 'youtu.be/' in url:
        return url.split('youtu.be/')[-1].split('?')[0]
    elif 'youtube.com' in url:
        parsed_url = urlparse(url)
        if 'v' in parse_qs(parsed_url.query):
            return parse_qs(parsed_url.query)['v'][0]
    return None

def format_filesize(bytes_size):
    """Format file size in human readable format"""
    if not bytes_size:
        return "Unknown"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def format_bitrate(bitrate):
    """Format bitrate in human readable format"""
    if not bitrate:
        return "Unknown"
    
    if bitrate >= 1000:
        return f"{bitrate/1000:.1f} Mbps"
    return f"{bitrate} kbps"

def analyze_video_quality(url, base_url="http://localhost:5000"):
    """Analyze video quality and provide recommendations"""
    
    print("🔍 YouTube Video Quality Analysis")
    print("=" * 60)
    
    video_id = extract_video_id(url)
    if video_id:
        print(f"📹 Video ID: {video_id}")
    
    print(f"🔗 URL: {url}")
    print("-" * 60)
    
    # Get video formats
    try:
        response = requests.post(f"{base_url}/formats", data={"url": url})
        
        if response.status_code != 200:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"❌ Error getting formats: {error_data}")
            return False
        
        data = response.json()
        
        # Basic info
        print(f"📺 Title: {data.get('title', 'Unknown')}")
        print(f"⏱️  Duration: {data.get('duration', 0)} seconds")
        print(f"👤 Uploader: {data.get('uploader', 'Unknown')}")
        print(f"👁️  Views: {data.get('view_count', 0):,}")
        print("-" * 60)
        
        # Video formats analysis
        video_formats = data.get('video_formats', [])
        audio_formats = data.get('audio_formats', [])
        
        if not video_formats:
            print("❌ No video formats available")
            return False
        
        print(f"🎬 VIDEO QUALITY ANALYSIS ({len(video_formats)} formats available)")
        print("-" * 60)
        
        # Group by resolution for better analysis
        resolution_groups = {}
        for fmt in video_formats:
            res = fmt.get('resolution', 'Unknown')
            if res not in resolution_groups:
                resolution_groups[res] = []
            resolution_groups[res].append(fmt)
        
        # Analyze each resolution
        best_overall = None
        best_overall_score = 0
        
        for resolution in sorted(resolution_groups.keys(), key=lambda x: int(x[:-1]) if x.endswith('p') and x[:-1].isdigit() else 0, reverse=True):
            formats = resolution_groups[resolution]
            best_format = max(formats, key=lambda x: x.get('tbr', 0) or 0)
            
            height = best_format.get('height', 0)
            width = best_format.get('width', 0)
            tbr = best_format.get('tbr', 0)
            vbr = best_format.get('vbr', 0)
            fps = best_format.get('fps', 0)
            filesize = best_format.get('filesize', 0)
            codec = best_format.get('vcodec', 'Unknown')
            format_id = best_format.get('format_id', 'Unknown')
            
            # Calculate quality score
            quality_score = height * (tbr or vbr or 1)
            if quality_score > best_overall_score:
                best_overall_score = quality_score
                best_overall = best_format
            
            # Quality assessment
            if height >= 2160:
                quality_label = "🏆 ULTRA (4K)"
                quality_desc = "Cinema quality, perfect for large screens"
            elif height >= 1440:
                quality_label = "🥇 EXCELLENT (2K)"
                quality_desc = "Excellent for gaming and content creation"
            elif height >= 1080:
                quality_label = "🥈 VERY GOOD (FHD)"
                quality_desc = "Standard HD, great for most uses"
            elif height >= 720:
                quality_label = "🥉 GOOD (HD)"
                quality_desc = "Good for mobile and smaller screens"
            elif height >= 480:
                quality_label = "📱 ACCEPTABLE (SD)"
                quality_desc = "Basic quality, mobile friendly"
            else:
                quality_label = "💾 LOW"
                quality_desc = "Low quality, for very slow connections"
            
            print(f"\n{quality_label}")
            print(f"   Resolution: {width}x{height} @ {fps}fps")
            print(f"   Bitrate: {format_bitrate(tbr)} (Video: {format_bitrate(vbr)})")
            print(f"   File Size: {format_filesize(filesize)}")
            print(f"   Codec: {codec}")
            print(f"   Format ID: {format_id}")
            print(f"   📝 {quality_desc}")
            
            # Multiple formats for same resolution?
            if len(formats) > 1:
                other_formats = [f for f in formats if f != best_format]
                print(f"   ℹ️  {len(other_formats)} other format(s) available for this resolution")
        
        print("\n" + "=" * 60)
        print("🎯 RECOMMENDATIONS")
        print("=" * 60)
        
        if best_overall:
            print(f"🏆 BEST OVERALL QUALITY:")
            print(f"   Use format_id: {best_overall.get('format_id')}")
            print(f"   Resolution: {best_overall.get('resolution')}")
            print(f"   Bitrate: {format_bitrate(best_overall.get('tbr'))}")
            print(f"   Expected size: {format_filesize(best_overall.get('filesize'))}")
        
        # Usage recommendations
        print(f"\n📱 FOR MOBILE VIEWING:")
        mobile_formats = [f for f in video_formats if f.get('height', 0) <= 720]
        if mobile_formats:
            mobile_best = max(mobile_formats, key=lambda x: x.get('tbr', 0) or 0)
            print(f"   Use: {mobile_best.get('resolution')} (format_id: {mobile_best.get('format_id')})")
        
        print(f"\n💻 FOR DESKTOP/LAPTOP:")
        desktop_formats = [f for f in video_formats if 720 <= f.get('height', 0) <= 1080]
        if desktop_formats:
            desktop_best = max(desktop_formats, key=lambda x: x.get('tbr', 0) or 0)
            print(f"   Use: {desktop_best.get('resolution')} (format_id: {desktop_best.get('format_id')})")
        
        print(f"\n🖥️  FOR LARGE SCREENS:")
        large_formats = [f for f in video_formats if f.get('height', 0) >= 1080]
        if large_formats:
            large_best = max(large_formats, key=lambda x: x.get('tbr', 0) or 0)
            print(f"   Use: {large_best.get('resolution')} (format_id: {large_best.get('format_id')})")
        
        # Audio analysis
        print("\n" + "=" * 60)
        print(f"🎵 AUDIO QUALITY ANALYSIS ({len(audio_formats)} formats available)")
        print("=" * 60)
        
        if audio_formats:
            for fmt in audio_formats:
                abr = fmt.get('abr', 0)
                codec = fmt.get('acodec', 'Unknown')
                filesize = fmt.get('filesize', 0)
                format_id = fmt.get('format_id', 'Unknown')
                
                if abr >= 320:
                    quality_label = "🏆 EXCELLENT"
                elif abr >= 256:
                    quality_label = "🥇 VERY GOOD"
                elif abr >= 192:
                    quality_label = "🥈 GOOD"
                elif abr >= 128:
                    quality_label = "🥉 ACCEPTABLE"
                else:
                    quality_label = "💾 LOW"
                
                print(f"{quality_label} - {abr} kbps ({codec}) - {format_filesize(filesize)} - ID: {format_id}")
        
        # Download commands
        print("\n" + "=" * 60)
        print("📥 DOWNLOAD COMMANDS")
        print("=" * 60)
        
        if best_overall:
            print("🎯 Best Quality Video:")
            print(f'curl -X POST {base_url}/download \\')
            print(f'  -d "url={url}" \\')
            print(f'  -d "format=mp4" \\')
            print(f'  -d "format_id={best_overall.get("format_id")}" \\')
            print(f'  --output "best_quality.mp4"')
        
        if audio_formats:
            best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))
            print(f"\n🎵 Best Quality Audio:")
            print(f'curl -X POST {base_url}/download \\')
            print(f'  -d "url={url}" \\')
            print(f'  -d "format=mp3" \\')
            print(f'  -d "audio_quality={int(best_audio.get("abr", 320))}" \\')
            print(f'  --output "best_audio.mp3"')
        
        # Auto best quality endpoint
        print(f"\n⚡ Auto Best Quality (Recommended):")
        print(f'curl -X POST {base_url}/download-best \\')
        print(f'  -d "url={url}" \\')
        print(f'  -d "format=mp4" \\')
        print(f'  -d "target_resolution=1080p" \\')
        print(f'  --output "auto_best.mp4"')
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Analyze YouTube video quality')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--server', default='http://localhost:5000', help='Server URL (default: http://localhost:5000)')
    
    args = parser.parse_args()
    
    if not args.url:
        print("❌ Please provide a YouTube URL")
        sys.exit(1)
    
    success = analyze_video_quality(args.url, args.server)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
