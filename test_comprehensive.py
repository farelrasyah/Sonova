#!/usr/bin/env python3
"""
Comprehensive API Test Suite untuk YouTube Downloader
Jalankan: python test_comprehensive.py
"""

import requests
import json
import time
import os
import sys
from urllib.parse import urlparse

class YouTubeAPITester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
    
    def test_health_check(self):
        """Test 1: Health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                expected_keys = ["message", "status", "version", "endpoints"]
                
                if all(key in data for key in expected_keys):
                    self.log_test("Health Check", True, 
                                f"API Version: {data.get('version')}")
                else:
                    self.log_test("Health Check", False, 
                                "Missing required keys in response")
            else:
                self.log_test("Health Check", False, 
                            f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Health Check", False, str(e))
    
    def test_video_info(self):
        """Test 2: Video info endpoint"""
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
            "https://youtu.be/dQw4w9WgXcQ",  # Short URL
        ]
        
        for url in test_urls:
            try:
                response = self.session.post(
                    f"{self.base_url}/info",
                    data={"url": url}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["title", "duration", "uploader"]
                    
                    if all(field in data for field in required_fields):
                        self.log_test(f"Video Info ({urlparse(url).netloc})", True,
                                    f"Title: {data.get('title', 'N/A')[:50]}...")
                    else:
                        self.log_test(f"Video Info ({urlparse(url).netloc})", False,
                                    "Missing required fields")
                else:
                    error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                    self.log_test(f"Video Info ({urlparse(url).netloc})", False,
                                f"HTTP {response.status_code}: {error_data.get('error', 'Unknown error')}")
                    
            except Exception as e:
                self.log_test(f"Video Info ({urlparse(url).netloc})", False, str(e))
    
    def test_invalid_urls(self):
        """Test 3: Invalid URL handling"""
        invalid_urls = [
            "https://google.com",
            "not-a-url",
            "https://youtube.com/invalid",
            "",
        ]
        
        for url in invalid_urls:
            try:
                response = self.session.post(
                    f"{self.base_url}/download",
                    data={"url": url, "format": "mp3"}
                )
                
                if response.status_code == 400:
                    self.log_test(f"Invalid URL Rejection ({url[:20]}...)", True,
                                "Properly rejected invalid URL")
                else:
                    self.log_test(f"Invalid URL Rejection ({url[:20]}...)", False,
                                f"Should return 400, got {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Invalid URL Rejection ({url[:20]}...)", False, str(e))
    
    def test_missing_parameters(self):
        """Test 4: Missing parameters handling"""
        test_cases = [
            {},  # No parameters
            {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},  # Missing format
            {"format": "mp3"},  # Missing URL
        ]
        
        for i, data in enumerate(test_cases):
            try:
                response = self.session.post(
                    f"{self.base_url}/download",
                    data=data
                )
                
                if response.status_code == 400:
                    self.log_test(f"Missing Parameters Test {i+1}", True,
                                "Properly rejected missing parameters")
                else:
                    self.log_test(f"Missing Parameters Test {i+1}", False,
                                f"Should return 400, got {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Missing Parameters Test {i+1}", False, str(e))
    
    def test_format_validation(self):
        """Test 5: Format validation"""
        invalid_formats = ["avi", "mkv", "wav", "flac", "invalid"]
        
        for format_type in invalid_formats:
            try:
                response = self.session.post(
                    f"{self.base_url}/download",
                    data={
                        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        "format": format_type
                    }
                )
                
                if response.status_code == 400:
                    self.log_test(f"Invalid Format ({format_type})", True,
                                "Properly rejected invalid format")
                else:
                    self.log_test(f"Invalid Format ({format_type})", False,
                                f"Should return 400, got {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Invalid Format ({format_type})", False, str(e))
    
    def test_mp3_download_simulation(self):
        """Test 6: MP3 download simulation (headers only)"""
        try:
            response = self.session.post(
                f"{self.base_url}/download",
                data={
                    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "format": "mp3"
                },
                stream=True
            )
            
            if response.status_code == 200:
                # Check headers
                content_type = response.headers.get('content-type', '')
                content_disposition = response.headers.get('content-disposition', '')
                
                if 'audio' in content_type and 'attachment' in content_disposition:
                    self.log_test("MP3 Download Headers", True,
                                f"Content-Type: {content_type}")
                    
                    # Don't actually download, just close the connection
                    response.close()
                else:
                    self.log_test("MP3 Download Headers", False,
                                "Invalid response headers")
            else:
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                self.log_test("MP3 Download Headers", False,
                            f"HTTP {response.status_code}: {error_data.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.log_test("MP3 Download Headers", False, str(e))
    
    def test_mp4_download_simulation(self):
        """Test 7: MP4 download simulation (headers only)"""
        try:
            response = self.session.post(
                f"{self.base_url}/download",
                data={
                    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "format": "mp4",
                    "resolution": "360p"
                },
                stream=True
            )
            
            if response.status_code == 200:
                # Check headers
                content_type = response.headers.get('content-type', '')
                content_disposition = response.headers.get('content-disposition', '')
                
                if 'video' in content_type and 'attachment' in content_disposition:
                    self.log_test("MP4 Download Headers", True,
                                f"Content-Type: {content_type}")
                    
                    # Don't actually download, just close the connection
                    response.close()
                else:
                    self.log_test("MP4 Download Headers", False,
                                "Invalid response headers")
            else:
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                self.log_test("MP4 Download Headers", False,
                            f"HTTP {response.status_code}: {error_data.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.log_test("MP4 Download Headers", False, str(e))
    
    def test_cors_headers(self):
        """Test 8: CORS headers"""
        try:
            # Options request
            response = self.session.options(f"{self.base_url}/download")
            
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers'
            ]
            
            found_cors = any(header in response.headers for header in cors_headers)
            
            if found_cors:
                self.log_test("CORS Headers", True,
                            "CORS headers present")
            else:
                self.log_test("CORS Headers", False,
                            "Missing CORS headers")
                
        except Exception as e:
            self.log_test("CORS Headers", False, str(e))
    
    def test_not_found_endpoint(self):
        """Test 9: 404 handling"""
        try:
            response = self.session.get(f"{self.base_url}/nonexistent")
            
            if response.status_code == 404:
                self.log_test("404 Handling", True,
                            "Properly returns 404 for non-existent endpoints")
            else:
                self.log_test("404 Handling", False,
                            f"Should return 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("404 Handling", False, str(e))
    
    def test_response_time(self):
        """Test 10: Response time"""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response_time < 2.0:  # Should respond within 2 seconds
                self.log_test("Response Time", True,
                            f"Response time: {response_time:.2f}s")
            else:
                self.log_test("Response Time", False,
                            f"Too slow: {response_time:.2f}s")
                
        except Exception as e:
            self.log_test("Response Time", False, str(e))
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 YouTube Downloader API - Comprehensive Test Suite")
        print("=" * 60)
        
        # Test API connectivity first
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code != 200:
                print(f"❌ API tidak dapat diakses di {self.base_url}")
                return
        except Exception as e:
            print(f"❌ Tidak dapat terhubung ke API: {e}")
            print("   Pastikan server berjalan di http://localhost:5000")
            return
        
        print(f"✅ API dapat diakses di {self.base_url}")
        print("-" * 60)
        
        # Run all tests
        tests = [
            self.test_health_check,
            self.test_video_info,
            self.test_invalid_urls,
            self.test_missing_parameters,
            self.test_format_validation,
            self.test_mp3_download_simulation,
            self.test_mp4_download_simulation,
            self.test_cors_headers,
            self.test_not_found_endpoint,
            self.test_response_time,
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_test(test.__name__, False, f"Test error: {e}")
            print()  # Add spacing between tests
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 Semua test berhasil! API siap untuk deployment.")
        else:
            print("\n⚠️  Beberapa test gagal. Periksa log di atas.")
            print("\nTest yang gagal:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  ❌ {result['test']}: {result['message']}")
        
        print("\n💡 Tips:")
        print("  - Pastikan ffmpeg sudah terinstall")
        print("  - Periksa koneksi internet")
        print("  - Gunakan URL YouTube yang valid")
        print("  - Buka test_frontend.html untuk testing manual")

def main():
    """Main function"""
    api_url = "http://localhost:5000"
    
    # Allow custom API URL
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    
    print(f"Testing API at: {api_url}")
    
    tester = YouTubeAPITester(api_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
