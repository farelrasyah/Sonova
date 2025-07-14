#!/usr/bin/env python3
"""
YouTube Downloader dengan Multiple Bypass Strategies
Solusi untuk mengatasi bot detection YouTube
"""

import os
import re
import time
import random
import requests
import subprocess
from urllib.parse import urlparse, parse_qs
import yt_dlp
from werkzeug.utils import secure_filename

class AdvancedYouTubeDownloader:
    """Advanced YouTube downloader with multiple bypass strategies"""
    
    def __init__(self):
        self.supported_formats = ['mp3', 'mp4']
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0'
        ]
        
    def validate_youtube_url(self, url):
        """Validate if URL is a valid YouTube URL"""
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube\.com/(watch\?v=|embed/|v/)|youtu\.be/)[\w-]+'
        )
        return bool(youtube_regex.match(url))
    
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL"""
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        elif 'youtube.com' in url:
            parsed_url = urlparse(url)
            if 'v' in parse_qs(parsed_url.query):
                return parse_qs(parsed_url.query)['v'][0]
        return None
    
    def get_base_options(self):
        """Get base yt-dlp options with anti-detection and quality optimization"""
        return {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'ignoreerrors': False,
            'user_agent': random.choice(self.user_agents),
            'referer': 'https://www.youtube.com/',
            'sleep_interval': random.uniform(1, 3),
            'max_sleep_interval': 10,
            'retries': 5,
            'fragment_retries': 5,
            'skip_unavailable_fragments': True,
            'http_chunk_size': 10485760,  # 10MB chunks
            'nocheckcertificate': False,
            'prefer_insecure': False,
            # Quality optimization settings
            'youtube_include_dash_manifest': True,
            'youtube_include_hls_manifest': True,
            'hls_prefer_native': True,
            'prefer_ffmpeg': True,
            'keepvideo': False,
            # Enhanced video quality settings
            'format_sort': [
                'res:1080',      # Prefer 1080p
                'fps:30',        # Prefer 30fps
                'vcodec:h264',   # Prefer H.264 for compatibility
                'acodec:aac',    # Prefer AAC for audio
                'tbr',           # Higher total bitrate
                'size',          # Larger file (usually better quality)
                'br',            # Higher bitrate
                'asr',           # Higher audio sample rate
            ],
            # Anti-detection headers
            'headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive': '300',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'DNT': '1'
            }
        }
    
    def try_with_different_strategies(self, url, download=False, output_path=None, format_type='mp3', resolution=None, format_id=None, audio_quality=None):
        """Try different strategies to bypass YouTube restrictions"""
        
        strategies = [
            self._strategy_basic,
            self._strategy_with_cookies,
            self._strategy_with_proxy_headers,
            self._strategy_alternative_extractor,
            self._strategy_mobile_user_agent
        ]
        
        for i, strategy in enumerate(strategies, 1):
            print(f"Trying strategy {i}/{len(strategies)}...")
            try:
                result = strategy(url, download, output_path, format_type, resolution, format_id, audio_quality)
                if result:
                    print(f"✅ Strategy {i} successful!")
                    return result
            except Exception as e:
                print(f"❌ Strategy {i} failed: {str(e)}")
                time.sleep(random.uniform(2, 5))  # Wait between attempts
        
        return None
    
    def _strategy_basic(self, url, download=False, output_path=None, format_type='mp3', resolution=None, format_id=None, audio_quality=None):
        """Basic strategy with standard options - Enhanced for maximum quality"""
        options = self.get_base_options()
        
        if download and output_path:
            if format_type == 'mp3':
                # Use high quality audio settings
                audio_quality = audio_quality or '320'
                options.update({
                    'format': 'bestaudio[acodec!*=opus]/bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:  # mp4 - Enhanced for crystal clear quality
                if format_id:
                    # Use specific format ID with best audio merge
                    options.update({
                        'format': f"{format_id}+bestaudio[acodec!*=opus]/best[format_id={format_id}]+bestaudio/best[format_id={format_id}]",
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4',
                        'postprocessors': [{
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4',
                        }]
                    })
                else:
                    # Enhanced resolution-based selection for maximum clarity
                    if resolution:
                        height = resolution[:-1] if resolution.endswith('p') else resolution
                        # Prioritize highest bitrate for the resolution, prefer h264 over vp9 for compatibility
                        format_selector = f"best[height={height}][vcodec^=avc1]/best[height={height}][vcodec^=h264]/best[height={height}][ext=mp4]/best[height<={height}][vcodec^=avc1]/best[height<={height}][vcodec^=h264]/best[height<={height}][ext=mp4]+bestaudio[acodec!*=opus]/best[height<={height}][ext=mp4]/best[ext=mp4]"
                    else:
                        # Default to best quality available with optimal codec selection
                        format_selector = "best[height>=1080][vcodec^=avc1]/best[height>=1080][vcodec^=h264]/best[height>=720][vcodec^=avc1]/best[height>=720][vcodec^=h264]/best[ext=mp4][vcodec^=avc1]/best[ext=mp4][vcodec^=h264]/best[ext=mp4]+bestaudio[acodec!*=opus]/best[ext=mp4]/best"
                    
                    options.update({
                        'format': format_selector,
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4',
                        'writesubtitles': False,
                        'writeautomaticsub': False,
                        'postprocessors': [{
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4',
                        }]
                    })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _strategy_with_cookies(self, url, download=False, output_path=None, format_type='mp3', resolution=None, format_id=None, audio_quality=None):
        """Strategy using cookie simulation - Enhanced for maximum quality"""
        options = self.get_base_options()
        options.update({
            'cookiefile': None,
            'headers': {
                **options.get('headers', {}),
                'Cookie': 'CONSENT=YES+cb.20210328-17-p0.en+FX+667; YSC=ABCdefGHIjkl; VISITOR_INFO1_LIVE=ABCdefGHIjkl'
            }
        })
        
        if download and output_path:
            if format_type == 'mp3':
                audio_quality = audio_quality or '320'
                options.update({
                    'format': 'bestaudio[acodec!*=opus]/bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:
                if format_id:
                    options.update({
                        'format': f"{format_id}+bestaudio[acodec!*=opus]/best[format_id={format_id}]+bestaudio/best[format_id={format_id}]",
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4',
                        'postprocessors': [{
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4',
                        }]
                    })
                else:
                    if resolution:
                        height = resolution[:-1] if resolution.endswith('p') else resolution
                        format_selector = f"best[height={height}][vcodec^=avc1]/best[height={height}][vcodec^=h264]/best[height={height}][ext=mp4]/best[height<={height}][vcodec^=avc1]/best[height<={height}][vcodec^=h264]/best[height<={height}][ext=mp4]+bestaudio[acodec!*=opus]/best[height<={height}][ext=mp4]/best[ext=mp4]"
                    else:
                        format_selector = "best[height>=1080][vcodec^=avc1]/best[height>=1080][vcodec^=h264]/best[height>=720][vcodec^=avc1]/best[height>=720][vcodec^=h264]/best[ext=mp4][vcodec^=avc1]/best[ext=mp4][vcodec^=h264]/best[ext=mp4]+bestaudio[acodec!*=opus]/best[ext=mp4]/best"
                    
                    options.update({
                        'format': format_selector,
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4',
                        'postprocessors': [{
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4',
                        }]
                    })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _strategy_with_proxy_headers(self, url, download=False, output_path=None, format_type='mp3', resolution=None, format_id=None, audio_quality=None):
        """Strategy with additional proxy-like headers"""
        options = self.get_base_options()
        options.update({
            'headers': {
                **options.get('headers', {}),
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'CF-Connecting-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            }
        })
        
        if download and output_path:
            if format_type == 'mp3':
                audio_quality = audio_quality or '320'
                options.update({
                    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:
                if format_id:
                    options.update({
                        'format': f"{format_id}+bestaudio[ext=m4a]/best[format_id={format_id}]",
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4'
                    })
                else:
                    if resolution:
                        height = resolution[:-1] if resolution.endswith('p') else resolution
                        format_selector = f"best[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best[ext=mp4]+bestaudio/best[ext=mp4]/best"
                    else:
                        format_selector = "best[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best+bestaudio/best"
                    
                    options.update({
                        'format': format_selector,
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4'
                    })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _strategy_alternative_extractor(self, url, download=False, output_path=None, format_type='mp3', resolution=None, format_id=None, audio_quality=None):
        """Strategy using alternative extractors"""
        options = self.get_base_options()
        options.update({
            'force_generic_extractor': False,
            'youtube_include_dash_manifest': False,
            'youtube_include_hls_manifest': False
        })
        
        if download and output_path:
            if format_type == 'mp3':
                audio_quality = audio_quality or '320'
                options.update({
                    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:
                if format_id:
                    options.update({
                        'format': f"{format_id}+bestaudio[ext=m4a]/best[format_id={format_id}]",
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4'
                    })
                else:
                    if resolution:
                        height = resolution[:-1] if resolution.endswith('p') else resolution
                        format_selector = f"best[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best[ext=mp4]+bestaudio/best[ext=mp4]/best"
                    else:
                        format_selector = "best[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best+bestaudio/best"
                    
                    options.update({
                        'format': format_selector,
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4'
                    })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _strategy_mobile_user_agent(self, url, download=False, output_path=None, format_type='mp3', resolution=None, format_id=None, audio_quality=None):
        """Strategy using mobile user agent"""
        options = self.get_base_options()
        options.update({
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'headers': {
                **options.get('headers', {}),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1'
            }
        })
        
        if download and output_path:
            if format_type == 'mp3':
                audio_quality = audio_quality or '320'
                options.update({
                    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:
                if format_id:
                    options.update({
                        'format': f"{format_id}+bestaudio[ext=m4a]/best[format_id={format_id}]",
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4'
                    })
                else:
                    if resolution:
                        height = resolution[:-1] if resolution.endswith('p') else resolution
                        format_selector = f"best[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best[ext=mp4]+bestaudio/best[ext=mp4]/best"
                    else:
                        format_selector = "best[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best+bestaudio/best"
                    
                    options.update({
                        'format': format_selector,
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4'
                    })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def get_video_info(self, url):
        """Get video information using multiple strategies"""
        if not self.validate_youtube_url(url):
            return None
        
        return self.try_with_different_strategies(url, download=False)
    
    def get_available_formats(self, url):
        """Get detailed information about available formats"""
        if not self.validate_youtube_url(url):
            return None
        
        try:
            info = self.get_video_info(url)
            if not info:
                return None
            
            formats = info.get('formats', [])
            video_formats = []
            audio_formats = []
            
            # Process video formats
            seen_video_qualities = {}
            for fmt in formats:
                if fmt.get('vcodec') and fmt.get('vcodec') != 'none':
                    height = fmt.get('height')
                    if height:
                        quality_key = f"{height}p"
                        
                        # Get the best quality for this resolution
                        current_quality = {
                            'resolution': quality_key,
                            'height': height,
                            'width': fmt.get('width'),
                            'ext': fmt.get('ext', 'mp4'),
                            'vcodec': fmt.get('vcodec'),
                            'acodec': fmt.get('acodec'),
                            'filesize': fmt.get('filesize'),
                            'tbr': fmt.get('tbr'),  # Total bitrate
                            'vbr': fmt.get('vbr'),  # Video bitrate
                            'abr': fmt.get('abr'),  # Audio bitrate
                            'fps': fmt.get('fps'),
                            'format_id': fmt.get('format_id'),
                            'format_note': fmt.get('format_note', ''),
                            'quality': fmt.get('quality', 0)
                        }
                        
                        # Keep the highest quality for each resolution
                        if quality_key not in seen_video_qualities or \
                           (current_quality['tbr'] and seen_video_qualities[quality_key]['tbr'] and 
                            current_quality['tbr'] > seen_video_qualities[quality_key]['tbr']):
                            seen_video_qualities[quality_key] = current_quality
            
            # Convert to list and sort by resolution
            video_formats = list(seen_video_qualities.values())
            video_formats.sort(key=lambda x: x['height'], reverse=True)
            
            # Process audio formats
            seen_audio_qualities = {}
            for fmt in formats:
                if fmt.get('acodec') and fmt.get('acodec') != 'none' and (not fmt.get('vcodec') or fmt.get('vcodec') == 'none'):
                    abr = fmt.get('abr', 0)
                    if abr:
                        quality_key = f"{int(abr)}kbps"
                        
                        current_quality = {
                            'quality': quality_key,
                            'abr': abr,
                            'ext': fmt.get('ext', 'mp3'),
                            'acodec': fmt.get('acodec'),
                            'filesize': fmt.get('filesize'),
                            'format_id': fmt.get('format_id'),
                            'format_note': fmt.get('format_note', '')
                        }
                        
                        if quality_key not in seen_audio_qualities or \
                           current_quality['abr'] > seen_audio_qualities[quality_key]['abr']:
                            seen_audio_qualities[quality_key] = current_quality
            
            audio_formats = list(seen_audio_qualities.values())
            audio_formats.sort(key=lambda x: x['abr'], reverse=True)
            
            return {
                'title': info.get('title'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'view_count': info.get('view_count'),
                'thumbnail': info.get('thumbnail'),
                'video_formats': video_formats,
                'audio_formats': audio_formats
            }
            
        except Exception as e:
            print(f"Error getting available formats: {e}")
            return None
    
    def download_audio(self, url, output_path, quality=None):
        """Download audio using multiple strategies with specified quality"""
        if not self.validate_youtube_url(url):
            return None, None
        
        try:
            info = self.try_with_different_strategies(url, download=True, output_path=output_path, format_type='mp3', audio_quality=quality)
            if info:
                title = info.get('title', 'audio')
                safe_title = secure_filename(title)
                
                # Find downloaded MP3 file
                for file in os.listdir(output_path):
                    if file.endswith('.mp3'):
                        actual_file = os.path.join(output_path, file)
                        expected_file = os.path.join(output_path, f"{safe_title}.mp3")
                        if actual_file != expected_file:
                            os.rename(actual_file, expected_file)
                        return expected_file, safe_title
                        
                return None, None
            return None, None
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None, None
    
    def download_video(self, url, output_path, resolution=None, format_id=None):
        """Download video using multiple strategies with high quality"""
        if not self.validate_youtube_url(url):
            return None, None
        
        try:
            # If format_id is specified, use it directly for best quality
            if format_id:
                info = self.try_with_different_strategies(url, download=True, output_path=output_path, format_type='mp4', resolution=resolution, format_id=format_id)
            else:
                info = self.try_with_different_strategies(url, download=True, output_path=output_path, format_type='mp4', resolution=resolution)
            
            if info:
                title = info.get('title', 'video')
                safe_title = secure_filename(title)
                
                # Find downloaded MP4 file
                for file in os.listdir(output_path):
                    if file.endswith('.mp4'):
                        actual_file = os.path.join(output_path, file)
                        expected_file = os.path.join(output_path, f"{safe_title}.mp4")
                        if actual_file != expected_file:
                            os.rename(actual_file, expected_file)
                        return expected_file, safe_title
                        
                return None, None
            return None, None
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None, None
    
    def get_best_format_for_resolution(self, url, target_resolution):
        """Get the best format ID for a specific resolution"""
        try:
            formats_info = self.get_available_formats(url)
            if not formats_info:
                return None
            
            video_formats = formats_info.get('video_formats', [])
            target_height = int(target_resolution[:-1]) if target_resolution.endswith('p') else int(target_resolution)
            
            # Find all formats for the target resolution
            matching_formats = [fmt for fmt in video_formats if fmt.get('height') == target_height]
            
            if not matching_formats:
                # If exact resolution not found, find the closest one below
                lower_formats = [fmt for fmt in video_formats if fmt.get('height', 0) <= target_height]
                if lower_formats:
                    matching_formats = [max(lower_formats, key=lambda x: x.get('height', 0))]
            
            if not matching_formats:
                return None
            
            # Sort by total bitrate (descending) to get best quality
            best_format = max(matching_formats, key=lambda x: x.get('tbr', 0) or 0)
            
            return {
                'format_id': best_format.get('format_id'),
                'resolution': f"{best_format.get('height')}p",
                'bitrate': best_format.get('tbr'),
                'codec': best_format.get('vcodec'),
                'fps': best_format.get('fps')
            }
            
        except Exception as e:
            print(f"Error getting best format: {e}")
            return None

    def download_with_best_quality(self, url, output_path, target_resolution=None):
        """Download video with automatically selected best quality"""
        try:
            # Get the best format for target resolution
            if target_resolution:
                best_format = self.get_best_format_for_resolution(url, target_resolution)
                if best_format:
                    print(f"🎯 Selected best format: {best_format['resolution']} at {best_format['bitrate']} kbps")
                    return self.download_video(url, output_path, target_resolution, best_format['format_id'])
            
            # Fallback to regular download with best available
            return self.download_video(url, output_path, target_resolution)
            
        except Exception as e:
            print(f"Error in best quality download: {e}")
            return None, None

# Test function
if __name__ == "__main__":
    downloader = AdvancedYouTubeDownloader()
    
    # Test URLs
    test_urls = [
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo
        "https://www.youtube.com/watch?v=BaW_jenozKc",  # YouTube Rewind 2018
    ]
    
    for url in test_urls:
        print(f"\n🧪 Testing: {url}")
        try:
            info = downloader.get_video_info(url)
            if info:
                print(f"✅ Success: {info.get('title', 'Unknown')}")
            else:
                print("❌ Failed to get info")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(5)  # Wait between tests
