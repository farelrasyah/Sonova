#!/bin/bash
# Enhanced YouTube Downloader - cURL Examples
# Contoh-contoh penggunaan API dengan berbagai kualitas

BASE_URL="http://localhost:5000"
TEST_VIDEO="https://www.youtube.com/watch?v=jNQXAC9IVRw"  # First YouTube video

echo "🎥 Enhanced YouTube Downloader - cURL Examples"
echo "=============================================="
echo ""

echo "📋 1. Get Basic Video Information"
echo "curl -X POST $BASE_URL/info -d \"url=$TEST_VIDEO\""
echo ""
curl -X POST $BASE_URL/info \
  -d "url=$TEST_VIDEO" \
  | python -m json.tool
echo ""
echo "=============================================="

echo "🔍 2. Get Detailed Format Information"
echo "curl -X POST $BASE_URL/formats -d \"url=$TEST_VIDEO\""
echo ""
curl -X POST $BASE_URL/formats \
  -d "url=$TEST_VIDEO" \
  | python -m json.tool | head -50
echo "... (truncated, run command to see full output)"
echo ""
echo "=============================================="

echo "📥 3. Download Examples"
echo ""

echo "🎬 3a. Download Best Available Quality (Auto)"
echo "curl -X POST $BASE_URL/download -d \"url=$TEST_VIDEO\" -d \"format=mp4\" --output auto_quality.mp4"
echo ""

echo "🎯 3b. Download Specific Resolution"
echo "curl -X POST $BASE_URL/download -d \"url=$TEST_VIDEO\" -d \"format=mp4\" -d \"resolution=720p\" --output 720p_video.mp4"
echo ""

echo "🎪 3c. Download with Specific Format ID (Best Quality)"
echo "# First get format info, then use specific format_id:"
echo "curl -X POST $BASE_URL/download -d \"url=$TEST_VIDEO\" -d \"format=mp4\" -d \"format_id=137\" --output hq_video.mp4"
echo ""

echo "🎵 3d. Download High Quality Audio"
echo "curl -X POST $BASE_URL/download -d \"url=$TEST_VIDEO\" -d \"format=mp3\" -d \"audio_quality=320\" --output hq_audio.mp3"
echo ""

echo "🔥 4. Quality Comparison Downloads"
echo ""

# Array of different quality settings to test
qualities=("2160p" "1440p" "1080p" "720p" "480p" "360p")
audio_qualities=("320" "256" "192" "128")

echo "🎬 Testing Video Qualities:"
for quality in "${qualities[@]}"; do
    filename="test_${quality}.mp4"
    echo "  📱 $quality: curl -X POST $BASE_URL/download -d \"url=$TEST_VIDEO\" -d \"format=mp4\" -d \"resolution=$quality\" --output $filename"
done

echo ""
echo "🎵 Testing Audio Qualities:"
for audio_quality in "${audio_qualities[@]}"; do
    filename="test_${audio_quality}kbps.mp3"
    echo "  🔊 ${audio_quality}kbps: curl -X POST $BASE_URL/download -d \"url=$TEST_VIDEO\" -d \"format=mp3\" -d \"audio_quality=$audio_quality\" --output $filename"
done

echo ""
echo "=============================================="
echo "💡 Advanced Usage Tips"
echo "=============================================="

echo ""
echo "🎯 Step-by-step for Maximum Quality:"
echo "1. Get format information:"
echo "   curl -X POST $BASE_URL/formats -d \"url=YOUR_URL\" > formats.json"
echo ""
echo "2. Find the highest bitrate format for your desired resolution"
echo "   cat formats.json | jq '.video_formats[] | select(.resolution==\"1080p\") | {resolution, tbr, format_id}'"
echo ""
echo "3. Download using specific format_id:"
echo "   curl -X POST $BASE_URL/download -d \"url=YOUR_URL\" -d \"format=mp4\" -d \"format_id=BEST_FORMAT_ID\" --output best_quality.mp4"

echo ""
echo "📊 Quality Selection Guide:"
echo "=============================================="
echo "🏆 4K/2160p  - Cinema quality, large files (15-45 Mbps)"
echo "🥇 1440p     - Great for gaming content (9-18 Mbps)"  
echo "🥈 1080p     - Standard HD, good balance (5-8 Mbps)"
echo "🥉 720p      - Mobile HD, smaller files (2.5-5 Mbps)"
echo "📱 480p      - Mobile standard (1-2.5 Mbps)"
echo "💾 360p      - Low bandwidth (0.5-1 Mbps)"
echo ""
echo "🎵 Audio Quality Guide:"
echo "🏆 320kbps   - Near-lossless, music production"
echo "🥇 256kbps   - High quality listening"
echo "🥈 192kbps   - Standard quality"  
echo "💾 128kbps   - Basic quality, space saving"

echo ""
echo "🔧 Common Parameters:"
echo "=============================================="
echo "url          - YouTube video URL (required)"
echo "format       - 'mp4' for video, 'mp3' for audio (required)"
echo "resolution   - '144p', '360p', '720p', '1080p', '1440p', '2160p'"
echo "format_id    - Specific format ID from /formats endpoint"
echo "audio_quality- '128', '192', '256', '320' (for mp3)"

echo ""
echo "⚡ Quick Test Commands:"
echo "=============================================="

echo ""
echo "🧪 Test Server Status:"
echo "curl $BASE_URL"

echo ""
echo "🧪 Test Video Info:"
echo "curl -X POST $BASE_URL/info -d \"url=$TEST_VIDEO\""

echo ""
echo "🧪 Download Sample 720p:"
echo "curl -X POST $BASE_URL/download -d \"url=$TEST_VIDEO\" -d \"format=mp4\" -d \"resolution=720p\" --output sample.mp4"

echo ""
echo "🧪 Download Sample Audio:"
echo "curl -X POST $BASE_URL/download -d \"url=$TEST_VIDEO\" -d \"format=mp3\" -d \"audio_quality=192\" --output sample.mp3"

echo ""
echo "=============================================="
echo "🎉 Ready to download high-quality videos!"
echo "Replace $TEST_VIDEO with your desired YouTube URL"
echo "=============================================="
