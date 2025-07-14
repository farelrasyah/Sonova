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
        """Get base yt-dlp options with anti-detection"""
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
            # Anti-detection headers
            'headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive': '300',
                'Connection': 'keep-alive',
            }
        }
    
    def try_with_different_strategies(self, url, download=False, output_path=None, format_type='mp3', resolution=None):
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
                result = strategy(url, download, output_path, format_type, resolution)
                if result:
                    print(f"✅ Strategy {i} successful!")
                    return result
            except Exception as e:
                print(f"❌ Strategy {i} failed: {str(e)}")
                time.sleep(random.uniform(2, 5))  # Wait between attempts
        
        return None
    
    def _strategy_basic(self, url, download=False, output_path=None, format_type='mp3', resolution=None):
        """Basic strategy with standard options"""
        options = self.get_base_options()
        
        if download and output_path:
            if format_type == 'mp3':
                options.update({
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:  # mp4
                format_selector = 'best[ext=mp4]/best'
                if resolution:
                    format_selector = f"best[height<={resolution[:-1]}][ext=mp4]/best[ext=mp4]"
                
                options.update({
                    'format': format_selector,
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4'
                })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _strategy_with_cookies(self, url, download=False, output_path=None, format_type='mp3', resolution=None):
        """Strategy using cookie simulation"""
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
                options.update({
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                format_selector = 'best[ext=mp4]/best'
                if resolution:
                    format_selector = f"best[height<={resolution[:-1]}][ext=mp4]/best[ext=mp4]"
                
                options.update({
                    'format': format_selector,
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4'
                })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _strategy_with_proxy_headers(self, url, download=False, output_path=None, format_type='mp3', resolution=None):
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
                options.update({
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                format_selector = 'best[ext=mp4]/best'
                if resolution:
                    format_selector = f"best[height<={resolution[:-1]}][ext=mp4]/best[ext=mp4]"
                
                options.update({
                    'format': format_selector,
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4'
                })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _strategy_alternative_extractor(self, url, download=False, output_path=None, format_type='mp3', resolution=None):
        """Strategy using alternative extractors"""
        options = self.get_base_options()
        options.update({
            'force_generic_extractor': False,
            'youtube_include_dash_manifest': False,
            'youtube_include_hls_manifest': False
        })
        
        if download and output_path:
            if format_type == 'mp3':
                options.update({
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                format_selector = 'best[ext=mp4]/best'
                if resolution:
                    format_selector = f"best[height<={resolution[:-1]}][ext=mp4]/best[ext=mp4]"
                
                options.update({
                    'format': format_selector,
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4'
                })
        
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _strategy_mobile_user_agent(self, url, download=False, output_path=None, format_type='mp3', resolution=None):
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
                options.update({
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                format_selector = 'best[ext=mp4]/best'
                if resolution:
                    format_selector = f"best[height<={resolution[:-1]}][ext=mp4]/best[ext=mp4]"
                
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
    
    def download_audio(self, url, output_path):
        """Download audio using multiple strategies"""
        if not self.validate_youtube_url(url):
            return None, None
        
        try:
            info = self.try_with_different_strategies(url, download=True, output_path=output_path, format_type='mp3')
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
    
    def download_video(self, url, output_path, resolution=None):
        """Download video using multiple strategies"""
        if not self.validate_youtube_url(url):
            return None, None
        
        try:
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
