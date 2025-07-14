#!/bin/bash

# Production deployment script untuk YouTube Downloader API

echo "🚀 Starting YouTube Downloader API deployment..."

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg not found. Please install ffmpeg first:"
    echo "   For Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   For CentOS/RHEL: sudo yum install ffmpeg"
    echo "   For macOS: brew install ffmpeg"
    echo "   For Windows: Download from https://ffmpeg.org/download.html"
    exit 1
fi

# Create necessary directories
mkdir -p temp
mkdir -p logs

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Start the application with gunicorn
echo "🔥 Starting application with Gunicorn..."
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 --access-logfile logs/access.log --error-logfile logs/error.log app:app

echo "✅ YouTube Downloader API is running on http://0.0.0.0:5000"
