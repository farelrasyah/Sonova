#!/usr/bin/env python3
"""
Auto-fix script untuk masalah umum YouTube Downloader
"""

import os
import sys
import shutil
import subprocess
import requests
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoFixer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.join(self.base_dir, 'temp')
        self.ffmpeg_dir = os.path.join(self.base_dir, 'ffmpeg')
    
    def fix_temp_directory(self):
        """Fix temp directory issues"""
        print("🔧 Fixing temp directory...")
        
        try:
            # Remove old temp directory if it exists
            if os.path.exists(self.temp_dir):
                print("📁 Removing old temp directory...")
                shutil.rmtree(self.temp_dir)
            
            # Create new temp directory
            print("📁 Creating new temp directory...")
            os.makedirs(self.temp_dir, exist_ok=True)
            
            # Set permissions (Windows)
            if os.name == 'nt':
                os.chmod(self.temp_dir, 0o777)
            
            # Create subdirectories for better organization
            for subdir in ['downloads', 'processing', 'cache']:
                subdir_path = os.path.join(self.temp_dir, subdir)
                os.makedirs(subdir_path, exist_ok=True)
            
            print("✅ Temp directory fixed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to fix temp directory: {e}")
            return False
    
    def fix_ffmpeg_path(self):
        """Fix FFmpeg path issues"""
        print("🔧 Fixing FFmpeg path...")
        
        try:
            # Check if FFmpeg exists in project directory
            ffmpeg_exe = os.path.join(self.ffmpeg_dir, 'ffmpeg.exe')
            ffmpeg_bin = os.path.join(self.ffmpeg_dir, 'ffmpeg-master-latest-win64-gpl', 'bin', 'ffmpeg.exe')
            
            if os.path.exists(ffmpeg_bin):
                print("📁 Found FFmpeg in project directory")
                # Copy to main ffmpeg directory
                shutil.copy2(ffmpeg_bin, ffmpeg_exe)
                print("✅ FFmpeg path fixed successfully")
                return True
            elif os.path.exists(ffmpeg_exe):
                print("✅ FFmpeg already in correct location")
                return True
            else:
                print("❌ FFmpeg not found in project directory")
                print("💡 Run: python setup_ffmpeg.py")
                return False
                
        except Exception as e:
            print(f"❌ Failed to fix FFmpeg path: {e}")
            return False
    
    def fix_cors_issues(self):
        """Fix CORS issues in app.py"""
        print("🔧 Fixing CORS issues...")
        
        try:
            app_py_path = os.path.join(self.base_dir, 'app.py')
            
            if not os.path.exists(app_py_path):
                print("❌ app.py not found")
                return False
            
            # Read current content
            with open(app_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if CORS is already properly configured
            if 'flask_cors' in content and 'origins="*"' in content:
                print("✅ CORS already configured correctly")
                return True
            
            # Add CORS configuration if missing
            if 'from flask_cors import CORS' not in content:
                print("📝 Adding CORS import...")
                content = content.replace(
                    'from flask import Flask',
                    'from flask import Flask\nfrom flask_cors import CORS'
                )
            
            if 'CORS(app' not in content:
                print("📝 Adding CORS configuration...")
                content = content.replace(
                    'app = Flask(__name__)',
                    'app = Flask(__name__)\nCORS(app, origins="*", methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type"])'
                )
            
            # Write back
            with open(app_py_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ CORS issues fixed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to fix CORS issues: {e}")
            return False
    
    def fix_permissions(self):
        """Fix file permissions"""
        print("🔧 Fixing file permissions...")
        
        try:
            # Fix permissions for key files
            key_files = [
                'app.py',
                'advanced_downloader.py',
                'youtube_bypass.py',
                'troubleshooting.py'
            ]
            
            for filename in key_files:
                filepath = os.path.join(self.base_dir, filename)
                if os.path.exists(filepath):
                    os.chmod(filepath, 0o644)
            
            # Fix permissions for directories
            key_dirs = [
                'temp',
                'ffmpeg',
                '__pycache__'
            ]
            
            for dirname in key_dirs:
                dirpath = os.path.join(self.base_dir, dirname)
                if os.path.exists(dirpath):
                    os.chmod(dirpath, 0o755)
            
            print("✅ File permissions fixed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to fix file permissions: {e}")
            return False
    
    def fix_python_packages(self):
        """Fix Python package issues"""
        print("🔧 Fixing Python packages...")
        
        try:
            # Install/update required packages
            packages = [
                'flask',
                'flask-cors',
                'yt-dlp',
                'requests',
                'python-dotenv'
            ]
            
            for package in packages:
                print(f"📦 Installing/updating {package}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '--upgrade', package
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"❌ Failed to install {package}: {result.stderr}")
                    return False
            
            print("✅ Python packages fixed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to fix Python packages: {e}")
            return False
    
    def fix_network_issues(self):
        """Fix network-related issues"""
        print("🔧 Fixing network issues...")
        
        try:
            # Test connectivity
            print("🌐 Testing internet connectivity...")
            response = requests.get('https://www.google.com', timeout=10)
            if response.status_code != 200:
                print("❌ No internet connection")
                return False
            
            print("🌐 Testing YouTube connectivity...")
            response = requests.get('https://www.youtube.com', timeout=10)
            if response.status_code != 200:
                print("❌ Cannot reach YouTube")
                return False
            
            print("✅ Network connectivity is working")
            return True
            
        except Exception as e:
            print(f"❌ Network test failed: {e}")
            return False
    
    def run_auto_fix(self):
        """Run all auto-fix procedures"""
        print("🚀 Starting Auto-Fix Process...")
        print("=" * 50)
        
        fixes = [
            ("Temp Directory", self.fix_temp_directory),
            ("FFmpeg Path", self.fix_ffmpeg_path),
            ("CORS Configuration", self.fix_cors_issues),
            ("File Permissions", self.fix_permissions),
            ("Python Packages", self.fix_python_packages),
            ("Network Issues", self.fix_network_issues),
        ]
        
        results = []
        for fix_name, fix_func in fixes:
            try:
                print(f"\n🔧 Running: {fix_name}")
                result = fix_func()
                results.append((fix_name, result))
                if result:
                    print(f"✅ {fix_name}: FIXED")
                else:
                    print(f"❌ {fix_name}: FAILED")
            except Exception as e:
                print(f"❌ {fix_name}: ERROR - {e}")
                results.append((fix_name, False))
        
        print("\n" + "=" * 50)
        print("📋 AUTO-FIX SUMMARY")
        print("=" * 50)
        
        fixed = sum(1 for _, result in results if result)
        total = len(results)
        
        for fix_name, result in results:
            status = "✅ FIXED" if result else "❌ FAILED"
            print(f"{fix_name}: {status}")
        
        print(f"\n📊 Overall: {fixed}/{total} fixes applied")
        
        if fixed == total:
            print("🎉 All fixes applied successfully!")
            print("💡 Try running the application again: python app.py")
        else:
            print("⚠️  Some fixes failed. Manual intervention may be required.")
        
        return fixed == total

def main():
    """Main function"""
    fixer = AutoFixer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'temp':
            fixer.fix_temp_directory()
        elif command == 'ffmpeg':
            fixer.fix_ffmpeg_path()
        elif command == 'cors':
            fixer.fix_cors_issues()
        elif command == 'permissions':
            fixer.fix_permissions()
        elif command == 'packages':
            fixer.fix_python_packages()
        elif command == 'network':
            fixer.fix_network_issues()
        else:
            print("Available commands: temp, ffmpeg, cors, permissions, packages, network")
    else:
        fixer.run_auto_fix()

if __name__ == "__main__":
    main()
