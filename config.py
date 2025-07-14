# YouTube Downloader API Configuration

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 5000
API_DEBUG = False

# File Upload Settings
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
UPLOAD_FOLDER = "temp"

# Download Settings
DOWNLOAD_TIMEOUT = 300  # 5 minutes
MAX_CONCURRENT_DOWNLOADS = 10

# Supported formats and resolutions
SUPPORTED_FORMATS = ["mp3", "mp4"]
SUPPORTED_RESOLUTIONS = ["144p", "240p", "360p", "480p", "720p", "1080p", "4k"]

# Audio quality settings
AUDIO_QUALITY = {
    "mp3": {
        "codec": "mp3",
        "bitrate": "192k",
        "sample_rate": "44100"
    }
}

# Video quality settings
VIDEO_QUALITY = {
    "mp4": {
        "codec": "libx264",
        "preset": "medium",
        "crf": "23"
    }
}

# Security settings
ALLOWED_HOSTS = ["*"]  # Sesuaikan dengan domain Anda
CORS_ORIGINS = ["*"]   # Sesuaikan dengan frontend domain

# Rate limiting (requests per minute)
RATE_LIMIT = {
    "download": 10,
    "info": 30
}

# Logging configuration
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": {
        "file": {
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        },
        "console": {
            "stream": "ext://sys.stdout"
        }
    }
}

# YouTube-DL options
YTDL_OPTIONS = {
    "format": "best",
    "noplaylist": True,
    "extractaudio": True,
    "audioformat": "mp3",
    "outtmpl": "%(title)s.%(ext)s",
    "restrictfilenames": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "extractflat": False,
    "writethumbnail": False,
    "writeinfojson": False,
    "writedescription": False,
    "writesubtitles": False,
    "writeautomaticsub": False,
    "allsubtitles": False,
    "listsubtitles": False,
    "subtitlesformat": "srt",
    "subtitleslangs": ["en", "id"],
    "matchtitle": None,
    "rejecttitle": None,
    "max_downloads": None,
    "min_filesize": None,
    "max_filesize": None,
    "min_views": None,
    "max_views": None,
    "daterange": None,
    "datebefore": None,
    "dateafter": None,
    "min_duration": None,
    "max_duration": None,
    "age_limit": None,
    "download_archive": None,
    "cookiefile": None,
    "nocheckcertificate": False,
    "prefer_insecure": False,
    "proxy": None,
    "socket_timeout": None,
    "bidi_workaround": None,
    "debug_printtraffic": False,
    "prefer_ffmpeg": True,
    "include_ads": False,
    "default_search": "auto",
    "youtube_include_dash_manifest": True,
    "encoding": None,
    "extract_flat": False,
    "mark_watched": False,
    "merge_output_format": None,
    "final_ext": None,
    "postprocessors": [],
    "progress_hooks": [],
    "match_filter": None,
    "no_color": False,
    "ffmpeg_location": None,
    "hls_prefer_native": None,
    "hls_use_mpegts": None,
    "external_downloader": None,
    "external_downloader_args": None,
    "postprocessor_args": None,
    "cn_verification_proxy": None,
    "geo_verification_proxy": None,
    "geo_bypass": None,
    "geo_bypass_country": None,
    "geo_bypass_ip_block": None,
    "playliststart": None,
    "playlistend": None,
    "playlist_items": None,
    "playlistreverse": None,
    "playlistrandom": None,
    "matchtitle": None,
    "rejecttitle": None,
    "logger": None,
    "logtostderr": False,
    "writedescription": False,
    "writeinfojson": False,
    "writeannotations": False,
    "writethumbnail": False,
    "allow_unplayable_formats": False,
    "ignore_no_formats_error": False,
    "format_sort": None,
    "format_sort_force": False,
    "allow_multiple_video_streams": False,
    "allow_multiple_audio_streams": False,
    "check_formats": None,
    "listformats": None,
    "outtmpl": "%(title)s.%(ext)s",
    "outtmpl_na_placeholder": "NA",
    "restrictfilenames": True,
    "trim_file_name": False,
    "windowsfilenames": False,
    "ignoreerrors": False,
    "force_generic_extractor": False,
    "ratelimit": None,
    "throttledratelimit": None,
    "retries": 10,
    "fragment_retries": 10,
    "skip_unavailable_fragments": True,
    "keep_fragments": False,
    "buffersize": 1024,
    "noresizebuffer": False,
    "http_chunk_size": None,
    "continuedl": True,
    "noprogress": False,
    "progress_with_newline": False,
    "playliststart": None,
    "playlistend": None,
    "playlist_items": None,
    "playlistreverse": None,
    "playlistrandom": None,
    "xattr_set_filesize": None,
    "external_downloader": None,
    "external_downloader_args": None,
    "postprocessor_args": None,
    "keepvideo": False,
    "daterange": None,
    "datebefore": None,
    "dateafter": None,
    "min_duration": None,
    "max_duration": None,
    "age_limit": None,
    "download_archive": None,
    "break_on_existing": False,
    "break_on_reject": False,
    "skip_playlist_after_errors": None,
    "cookiefile": None,
    "nocheckcertificate": False,
    "prefer_insecure": False,
    "proxy": None,
    "socket_timeout": None,
    "bidi_workaround": None,
    "debug_printtraffic": False,
    "prefer_ffmpeg": True,
    "include_ads": False,
    "default_search": "auto",
    "youtube_include_dash_manifest": True,
    "encoding": None,
    "extract_flat": False,
    "mark_watched": False,
    "merge_output_format": None,
    "final_ext": None,
    "postprocessors": [],
    "progress_hooks": [],
    "match_filter": None,
    "no_color": False,
    "ffmpeg_location": None,
    "hls_prefer_native": None,
    "hls_use_mpegts": None,
    "cn_verification_proxy": None,
    "geo_verification_proxy": None,
    "geo_bypass": None,
    "geo_bypass_country": None,
    "geo_bypass_ip_block": None
}
