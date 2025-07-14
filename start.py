#!/usr/bin/env python3
"""
Start script untuk YouTube Downloader API
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 atau lebih baru diperlukan!")
        print(f"   Versi saat ini: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ffmpeg is installed")
            return True
        else:
            print("❌ ffmpeg not working properly")
            return False
    except FileNotFoundError:
        print("❌ ffmpeg not found!")
        print("   Install ffmpeg:")
        if platform.system() == "Windows":
            print("   - Download from https://ffmpeg.org/download.html")
            print("   - Extract and add to PATH")
        elif platform.system() == "Darwin":  # macOS
            print("   - Run: brew install ffmpeg")
        else:  # Linux
            print("   - Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("   - CentOS/RHEL: sudo yum install ffmpeg")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['temp', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def start_development_server():
    """Start development server"""
    print("🚀 Starting development server...")
    print("   Access the API at: http://localhost:5000")
    print("   Open test_frontend.html in browser to test")
    print("   Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def start_production_server():
    """Start production server with gunicorn"""
    print("🚀 Starting production server...")
    print("   Access the API at: http://localhost:5000")
    print("   Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            '-c', 'gunicorn.conf.py',
            'app:app'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    """Main function"""
    print("🎵 YouTube Downloader API Setup")
    print("=" * 40)
    
    # Check system requirements
    check_python_version()
    
    if not check_ffmpeg():
        sys.exit(1)
    
    # Setup
    create_directories()
    
    if not install_dependencies():
        sys.exit(1)
    
    # Ask for server type
    print("\n🔧 Choose server type:")
    print("1. Development (Flask dev server)")
    print("2. Production (Gunicorn)")
    
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice == '1':
            start_development_server()
            break
        elif choice == '2':
            start_production_server()
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
