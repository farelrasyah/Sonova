import os
import re
import tempfile
import logging
from urllib.parse import urlparse, parse_qs
from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import yt_dlp
from werkzeug.utils import secure_filename
import shutil

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for all domains (sesuaikan dengan kebutuhan production)
CORS(app, origins="*", methods=["GET", "POST"], allow_headers=["Content-Type"])

# Configuration
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 524288000))  # 500MB
TEMP_FOLDER = os.getenv('TEMP_FOLDER', './temp')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure temp directory exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

class YouTubeDownloader:
    """YouTube downloader class using yt-dlp"""
    
    def __init__(self):
        self.supported_formats = ['mp3', 'mp4']
        self.resolution_mapping = {
            '140p': '160',
            '240p': '133',
            '360p': '134',
            '480p': '135',
            '720p': '136',
            '1080p': '137',
            '4k': '313'
        }
    
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
    
    def get_video_info(self, url):
        """Get video information and available formats"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            return None
    
    def download_audio(self, url, output_path):
        """Download audio and convert to MP3"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'audio')
                safe_title = secure_filename(title)
                expected_file = os.path.join(output_path, f"{safe_title}.mp3")
                
                # Find the actual downloaded file
                for file in os.listdir(output_path):
                    if file.endswith('.mp3'):
                        actual_file = os.path.join(output_path, file)
                        if actual_file != expected_file:
                            os.rename(actual_file, expected_file)
                        return expected_file, safe_title
                        
                return None, None
        except Exception as e:
            logger.error(f"Error downloading audio: {str(e)}")
            return None, None
    
    def download_video(self, url, output_path, resolution=None):
        """Download video with specified resolution"""
        # Determine format selection based on resolution
        if resolution and resolution in self.resolution_mapping:
            format_selector = f"best[height<={resolution[:-1]}]"
        else:
            format_selector = 'best[ext=mp4]'
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'video')
                safe_title = secure_filename(title)
                expected_file = os.path.join(output_path, f"{safe_title}.mp4")
                
                # Find the actual downloaded file
                for file in os.listdir(output_path):
                    if file.endswith('.mp4'):
                        actual_file = os.path.join(output_path, file)
                        if actual_file != expected_file:
                            os.rename(actual_file, expected_file)
                        return actual_file, safe_title
                        
                return None, None
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            return None, None

# Initialize downloader
downloader = YouTubeDownloader()

@app.route('/', methods=['GET'])
def index():
    """Health check endpoint"""
    return jsonify({
        "message": "YouTube Downloader API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "download": "POST /download"
        }
    })

@app.route('/download', methods=['POST'])
def download_video():
    """Main download endpoint"""
    try:
        # Validate request
        if 'url' not in request.form:
            return jsonify({"error": "URL is required"}), 400
        
        if 'format' not in request.form:
            return jsonify({"error": "Format is required (mp3 or mp4)"}), 400
        
        url = request.form['url'].strip()
        format_type = request.form['format'].lower().strip()
        resolution = request.form.get('resolution', '').strip()
        
        # Validate inputs
        if not downloader.validate_youtube_url(url):
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        if format_type not in downloader.supported_formats:
            return jsonify({"error": "Format must be 'mp3' or 'mp4'"}), 400
        
        # Log request
        logger.info(f"Download request: URL={url}, Format={format_type}, Resolution={resolution}")
        
        # Create temporary directory for this download
        temp_dir = tempfile.mkdtemp(dir=TEMP_FOLDER)
        
        try:
            # Get video info first
            video_info = downloader.get_video_info(url)
            if not video_info:
                return jsonify({"error": "Unable to extract video information"}), 400
            
            # Download based on format
            if format_type == 'mp3':
                file_path, title = downloader.download_audio(url, temp_dir)
                if not file_path or not os.path.exists(file_path):
                    return jsonify({"error": "Failed to download audio"}), 500
                
                filename = f"{title}.mp3"
                mimetype = 'audio/mpeg'
                
            elif format_type == 'mp4':
                file_path, title = downloader.download_video(url, temp_dir, resolution)
                if not file_path or not os.path.exists(file_path):
                    return jsonify({"error": "Failed to download video"}), 500
                
                filename = f"{title}.mp4"
                mimetype = 'video/mp4'
            
            # Send file
            def cleanup():
                """Cleanup temp directory after sending file"""
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp directory: {e}")
            
            response = make_response(send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype=mimetype
            ))
            
            # Add headers
            response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
            response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
            
            # Schedule cleanup (in production, use background task)
            # cleanup()  # Commented out for now to ensure file is sent properly
            
            logger.info(f"Successfully downloaded: {filename}")
            return response
            
        except Exception as e:
            # Cleanup on error
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            raise e
            
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/info', methods=['POST'])
def get_video_info():
    """Get video information without downloading"""
    try:
        if 'url' not in request.form:
            return jsonify({"error": "URL is required"}), 400
        
        url = request.form['url'].strip()
        
        if not downloader.validate_youtube_url(url):
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        video_info = downloader.get_video_info(url)
        if not video_info:
            return jsonify({"error": "Unable to extract video information"}), 400
        
        # Extract relevant information
        info = {
            "title": video_info.get('title', 'Unknown'),
            "duration": video_info.get('duration', 0),
            "uploader": video_info.get('uploader', 'Unknown'),
            "view_count": video_info.get('view_count', 0),
            "upload_date": video_info.get('upload_date', ''),
            "description": video_info.get('description', '')[:200] + '...' if video_info.get('description') else '',
            "thumbnail": video_info.get('thumbnail', ''),
            "available_formats": []
        }
        
        # Get available formats
        formats = video_info.get('formats', [])
        seen_heights = set()
        for fmt in formats:
            if fmt.get('height') and fmt.get('height') not in seen_heights:
                info['available_formats'].append({
                    "resolution": f"{fmt.get('height')}p",
                    "ext": fmt.get('ext', ''),
                    "filesize": fmt.get('filesize')
                })
                seen_heights.add(fmt.get('height'))
        
        # Sort by resolution
        info['available_formats'].sort(key=lambda x: int(x['resolution'][:-1]), reverse=True)
        
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Info error: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info(f"Starting YouTube Downloader API on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
