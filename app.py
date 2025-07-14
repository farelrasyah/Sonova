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
from advanced_downloader import AdvancedYouTubeDownloader
from advanced_downloader import AdvancedYouTubeDownloader
from youtube_bypass import YouTubeBypasser

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

# Initialize advanced downloader
downloader = AdvancedYouTubeDownloader()

@app.route('/', methods=['GET'])
def index():
    """Health check endpoint"""
    return jsonify({
        "message": "Enhanced YouTube Downloader API",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "High-quality video downloads",
            "Multiple resolution options",
            "Detailed format information",
            "Audio quality selection",
            "Original quality preservation"
        ],
        "endpoints": {
            "download": "POST /download - Download video/audio with quality options",
            "info": "POST /info - Get basic video information",
            "formats": "POST /formats - Get detailed available formats"
        },
        "parameters": {
            "download": {
                "required": ["url", "format"],
                "optional": ["resolution", "format_id", "audio_quality"],
                "format_options": ["mp3", "mp4"],
                "audio_quality_options": ["128", "192", "256", "320"],
                "example_resolutions": ["144p", "360p", "720p", "1080p", "1440p", "2160p"]
            }
        }
    })

@app.route('/download', methods=['POST'])
def download_video():
    """Main download endpoint with enhanced quality options"""
    try:
        # Validate request
        if 'url' not in request.form:
            return jsonify({"error": "URL is required"}), 400
        
        if 'format' not in request.form:
            return jsonify({"error": "Format is required (mp3 or mp4)"}), 400
        
        url = request.form['url'].strip()
        format_type = request.form['format'].lower().strip()
        resolution = request.form.get('resolution', '').strip()
        format_id = request.form.get('format_id', '').strip()
        audio_quality = request.form.get('audio_quality', '').strip()
        
        # Validate inputs
        if not downloader.validate_youtube_url(url):
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        if format_type not in downloader.supported_formats:
            return jsonify({"error": "Format must be 'mp3' or 'mp4'"}), 400
        
        # Log request
        logger.info(f"Download request: URL={url}, Format={format_type}, Resolution={resolution}, Format_ID={format_id}, Audio_Quality={audio_quality}")
        
        # Create temporary directory for this download
        temp_dir = tempfile.mkdtemp(dir=TEMP_FOLDER)
        
        try:
            # Get video info first
            logger.info(f"Getting video info for: {url}")
            video_info = downloader.get_video_info(url)
            if not video_info:
                logger.error("Unable to extract video information")
                return jsonify({"error": "Unable to extract video information", "details": "The video may be private, deleted, or geo-blocked"}), 400
            
            logger.info(f"Video info extracted successfully: {video_info.get('title', 'Unknown')}")
            
            # Download based on format
            if format_type == 'mp3':
                logger.info(f"Starting MP3 download with quality: {audio_quality or 'best'}")
                file_path, title = downloader.download_audio(url, temp_dir, audio_quality)
                if not file_path or not os.path.exists(file_path):
                    logger.error("Failed to download audio")
                    return jsonify({"error": "Failed to download audio", "details": "Audio extraction failed"}), 500
                
                filename = f"{title}.mp3"
                mimetype = 'audio/mpeg'
                
            elif format_type == 'mp4':
                logger.info(f"Starting MP4 download with resolution: {resolution or 'best'}, format_id: {format_id or 'auto'}")
                file_path, title = downloader.download_video(url, temp_dir, resolution, format_id)
                if not file_path or not os.path.exists(file_path):
                    logger.error("Failed to download video")
                    return jsonify({"error": "Failed to download video", "details": "Video download failed"}), 500
                
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

@app.route('/formats', methods=['POST'])
def get_available_formats():
    """Get detailed available formats for a video"""
    try:
        if 'url' not in request.form:
            return jsonify({"error": "URL is required"}), 400
        
        url = request.form['url'].strip()
        
        if not downloader.validate_youtube_url(url):
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        logger.info(f"Getting formats for: {url}")
        formats_info = downloader.get_available_formats(url)
        
        if not formats_info:
            return jsonify({"error": "Unable to extract format information"}), 400
        
        logger.info(f"Found {len(formats_info.get('video_formats', []))} video formats and {len(formats_info.get('audio_formats', []))} audio formats")
        
        return jsonify(formats_info)
        
    except Exception as e:
        logger.error(f"Formats error: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/download-best', methods=['POST'])
def download_best_quality():
    """Download with automatically selected best quality"""
    try:
        # Validate request
        if 'url' not in request.form:
            return jsonify({"error": "URL is required"}), 400
        
        if 'format' not in request.form:
            return jsonify({"error": "Format is required (mp3 or mp4)"}), 400
        
        url = request.form['url'].strip()
        format_type = request.form['format'].lower().strip()
        target_resolution = request.form.get('target_resolution', '').strip()
        
        # Validate inputs
        if not downloader.validate_youtube_url(url):
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        if format_type not in downloader.supported_formats:
            return jsonify({"error": "Format must be 'mp3' or 'mp4'"}), 400
        
        # Log request
        logger.info(f"Best quality download request: URL={url}, Format={format_type}, Target={target_resolution or 'auto'}")
        
        # Create temporary directory for this download
        temp_dir = tempfile.mkdtemp(dir=TEMP_FOLDER)
        
        try:
            # Get video info first
            logger.info(f"Getting video info for: {url}")
            video_info = downloader.get_video_info(url)
            if not video_info:
                logger.error("Unable to extract video information")
                return jsonify({"error": "Unable to extract video information", "details": "The video may be private, deleted, or geo-blocked"}), 400
            
            logger.info(f"Video info extracted successfully: {video_info.get('title', 'Unknown')}")
            
            # Download with best quality selection
            if format_type == 'mp3':
                logger.info("Starting best quality MP3 download...")
                file_path, title = downloader.download_audio(url, temp_dir, '320')  # Always use 320kbps for best
            elif format_type == 'mp4':
                logger.info(f"Starting best quality MP4 download with target: {target_resolution or 'highest available'}")
                file_path, title = downloader.download_with_best_quality(url, temp_dir, target_resolution)
            
            if not file_path or not os.path.exists(file_path):
                logger.error("Failed to download with best quality")
                return jsonify({"error": "Failed to download with best quality", "details": "Download failed despite quality optimization"}), 500
            
            filename = f"{title}.{format_type}"
            mimetype = 'audio/mpeg' if format_type == 'mp3' else 'video/mp4'
            
            # Send file
            response = make_response(send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype=mimetype
            ))
            
            # Add headers
            response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
            response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
            
            logger.info(f"Successfully downloaded with best quality: {filename}")
            return response
            
        except Exception as e:
            # Cleanup on error
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            raise e
            
    except Exception as e:
        logger.error(f"Best quality download error: {str(e)}")
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
