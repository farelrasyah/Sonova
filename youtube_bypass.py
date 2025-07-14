#!/usr/bin/env python3
"""
YouTube Bot Detection Bypass Module
"""

import os
import tempfile
import random
import time
import requests
from urllib.parse import urlparse, parse_qs
import yt_dlp

class YouTubeBypasser:
    """Enhanced YouTube downloader with bot detection bypass"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
        ]
        
        self.referers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://duckduckgo.com/',
            'https://www.youtube.com/',
            'https://twitter.com/',
        ]
    
    def get_random_headers(self):
        """Get random headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Referer': random.choice(self.referers),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def create_cookies_file(self):
        """Create a temporary cookies file"""
        cookies_content = """# Netscape HTTP Cookie File
# This is a generated file!  Do not edit.

.youtube.com	TRUE	/	FALSE	0	CONSENT	YES+cb
.youtube.com	TRUE	/	FALSE	0	VISITOR_INFO1_LIVE	random_visitor_id
"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_file.write(cookies_content)
        temp_file.close()
        return temp_file.name
    
    def get_enhanced_ydl_opts(self, download=False):
        """Get enhanced yt-dlp options with bypass techniques"""
        headers = self.get_random_headers()
        cookies_file = self.create_cookies_file()
        
        opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True,
            
            # Headers and user agent
            'http_headers': headers,
            
            # Cookies
            'cookiefile': cookies_file,
            
            # Network settings
            'socket_timeout': 30,
            'retries': 5,
            'fragment_retries': 5,
            
            # Rate limiting
            'sleep_interval': random.uniform(1, 3),
            'max_sleep_interval': 8,
            
            # YouTube specific
            'youtube_include_dash_manifest': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            
            # Extractor args
            'extractor_args': {
                'youtube': {
                    'skip': ['hls', 'dash'],
                    'player_skip': ['js'],
                    'comment_sort': ['top'],
                    'max_comments': [0],
                }
            }
        }
        
        if not download:
            opts['simulate'] = True
            opts['skip_download'] = True
        
        return opts, cookies_file
    
    def extract_info_safe(self, url):
        """Safely extract video information with multiple fallback methods"""
        methods = [
            self._method_standard,
            self._method_no_playlist,
            self._method_generic,
            self._method_minimal,
        ]
        
        for i, method in enumerate(methods):
            try:
                print(f"Trying method {i+1}...")
                info = method(url)
                if info:
                    return info
                time.sleep(random.uniform(1, 2))
            except Exception as e:
                print(f"Method {i+1} failed: {str(e)}")
                time.sleep(random.uniform(2, 4))
        
        return None
    
    def _method_standard(self, url):
        """Standard extraction method"""
        opts, cookies_file = self.get_enhanced_ydl_opts()
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(url, download=False)
        finally:
            if os.path.exists(cookies_file):
                os.unlink(cookies_file)
    
    def _method_no_playlist(self, url):
        """Method with no playlist extraction"""
        opts, cookies_file = self.get_enhanced_ydl_opts()
        opts['noplaylist'] = True
        opts['extract_flat'] = True
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(url, download=False)
        finally:
            if os.path.exists(cookies_file):
                os.unlink(cookies_file)
    
    def _method_generic(self, url):
        """Generic extractor method"""
        opts, cookies_file = self.get_enhanced_ydl_opts()
        opts['force_generic_extractor'] = True
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(url, download=False)
        finally:
            if os.path.exists(cookies_file):
                os.unlink(cookies_file)
    
    def _method_minimal(self, url):
        """Minimal extraction method"""
        opts = {
            'quiet': True,
            'simulate': True,
            'skip_download': True,
            'http_headers': self.get_random_headers(),
        }
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(url, download=False)
        except:
            return None
    
    def download_safe(self, url, output_path, format_type='mp3', resolution=None):
        """Safely download video/audio with bypass techniques"""
        opts, cookies_file = self.get_enhanced_ydl_opts(download=True)
        
        if format_type == 'mp3':
            opts.update({
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:  # mp4
            if resolution:
                height = resolution.replace('p', '')
                opts['format'] = f'best[height<={height}]/best'
            else:
                opts['format'] = 'best[ext=mp4]/best'
            
            opts.update({
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
            })
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    title = info.get('title', 'download')
                    # Find downloaded file
                    for file in os.listdir(output_path):
                        if file.endswith(f'.{format_type}'):
                            return os.path.join(output_path, file), title
                return None, None
        except Exception as e:
            print(f"Download error: {e}")
            return None, None
        finally:
            if os.path.exists(cookies_file):
                os.unlink(cookies_file)


def test_bypass():
    """Test the bypass functionality"""
    bypasser = YouTubeBypasser()
    
    # Test URLs (use different videos)
    test_urls = [
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Gangnam Style
        "https://youtu.be/kJQP7kiw5Fk",  # Despacito
    ]
    
    for url in test_urls:
        print(f"\n🧪 Testing URL: {url}")
        info = bypasser.extract_info_safe(url)
        if info:
            print(f"✅ Success: {info.get('title', 'Unknown')}")
            break
        else:
            print(f"❌ Failed to extract info")
    
    return info is not None


if __name__ == "__main__":
    test_bypass()
