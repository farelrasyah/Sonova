# 🔧 Troubleshooting Kualitas Video Buruk

Panduan lengkap untuk mengatasi masalah video download yang masih buruk dan tidak jelas.

## 🚨 Diagnosa Masalah

### 1. Cek Kualitas yang Tersedia
```bash
python quality_analyzer.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

**Output yang perlu diperhatikan:**
- ✅ Apakah ada format 1080p atau 720p?
- ✅ Berapa bitrate tertinggi yang tersedia?
- ✅ Format ID mana yang terbaik?

### 2. Test Download Kualitas
```bash
python test_quality_verification.py
```

## 🎯 Solusi Step-by-Step

### Langkah 1: Gunakan Endpoint `/download-best`
```bash
curl -X POST http://localhost:5000/download-best \
  -d "url=YOUR_YOUTUBE_URL" \
  -d "format=mp4" \
  -d "target_resolution=1080p" \
  --output video_hd.mp4
```

### Langkah 2: Jika Masih Buruk, Cek Format Manual
```bash
# 1. Dapatkan daftar format
curl -X POST http://localhost:5000/formats \
  -d "url=YOUR_YOUTUBE_URL" > formats.json

# 2. Cari format_id dengan bitrate tertinggi
cat formats.json | grep -A5 -B5 "1080p"

# 3. Download dengan format_id spesifik
curl -X POST http://localhost:5000/download \
  -d "url=YOUR_YOUTUBE_URL" \
  -d "format=mp4" \
  -d "format_id=FORMAT_ID_TERBAIK" \
  --output video_specific.mp4
```

### Langkah 3: Verifikasi Kualitas Hasil
```bash
# Cek resolusi aktual (butuh ffprobe)
ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height,bit_rate,codec_name -of csv=p=0 video_hd.mp4

# Atau lihat ukuran file
ls -lh video_hd.mp4
```

## 🔍 Identifikasi Masalah Umum

### Masalah 1: Video Masih 480p atau Lebih Rendah
**Penyebab:**
- Video asli memang tidak tersedia dalam HD
- Format selector tidak optimal
- YouTube membatasi kualitas untuk video tertentu

**Solusi:**
```bash
# Cek apakah HD tersedia
python quality_analyzer.py "YOUR_URL"

# Jika HD tersedia, paksa gunakan format HD
curl -X POST http://localhost:5000/formats -d "url=YOUR_URL" | jq '.video_formats[] | select(.height >= 720)'

# Download dengan format_id HD terbaik
curl -X POST http://localhost:5000/download \
  -d "url=YOUR_URL" \
  -d "format=mp4" \
  -d "format_id=BEST_HD_FORMAT_ID" \
  --output hd_video.mp4
```

### Masalah 2: Video Buram/Pixelated Meskipun Resolusi Tinggi
**Penyebab:**
- Bitrate terlalu rendah
- Codec tidak optimal
- Video asli berkualitas buruk

**Solusi:**
```bash
# Cari format dengan bitrate tertinggi
curl -X POST http://localhost:5000/formats -d "url=YOUR_URL" | jq '.video_formats | sort_by(.tbr) | reverse | .[0]'

# Download dengan bitrate optimal
curl -X POST http://localhost:5000/download \
  -d "url=YOUR_URL" \
  -d "format=mp4" \
  -d "format_id=HIGH_BITRATE_FORMAT_ID" \
  --output high_bitrate.mp4
```

### Masalah 3: Audio dan Video Tidak Sinkron
**Penyebab:**
- Masalah merge audio+video
- Format tidak kompatibel

**Solusi:**
```bash
# Gunakan format yang sudah include audio
curl -X POST http://localhost:5000/formats -d "url=YOUR_URL" | jq '.video_formats[] | select(.acodec != null and .acodec != "none")'

# Atau download video dan audio terpisah lalu merge manual
```

### Masalah 4: File Size Terlalu Kecil untuk Kualitas yang Diklaim
**Penyebab:**
- Download tidak complete
- Format terkompresi berlebihan

**Solusi:**
```bash
# Cek expected file size dari API
curl -X POST http://localhost:5000/formats -d "url=YOUR_URL" | jq '.video_formats[] | {resolution, filesize, tbr}'

# Compare dengan file yang didownload
ls -l downloaded_video.mp4
```

## ⚡ Quick Fixes

### Fix 1: Force Best Quality Download
```python
# Gunakan script ini untuk download kualitas terbaik
import requests

url = "YOUR_YOUTUBE_URL"
base_url = "http://localhost:5000"

# Get best format
formats_response = requests.post(f"{base_url}/formats", data={"url": url})
formats = formats_response.json()

best_video = max(formats['video_formats'], key=lambda x: x.get('tbr', 0))
print(f"Best format: {best_video['resolution']} at {best_video['tbr']} kbps")

# Download with best format
download_response = requests.post(f"{base_url}/download", data={
    "url": url,
    "format": "mp4", 
    "format_id": best_video['format_id']
}, stream=True)

with open("best_quality.mp4", "wb") as f:
    for chunk in download_response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### Fix 2: Batch Quality Test
```bash
#!/bin/bash
# Test multiple resolutions untuk video yang sama

URL="YOUR_YOUTUBE_URL"
RESOLUTIONS=("2160p" "1440p" "1080p" "720p")

for res in "${RESOLUTIONS[@]}"; do
    echo "Testing $res..."
    curl -X POST http://localhost:5000/download-best \
        -d "url=$URL" \
        -d "format=mp4" \
        -d "target_resolution=$res" \
        --output "test_${res}.mp4"
    
    # Check file size
    ls -lh "test_${res}.mp4"
done
```

## 🛠️ Advanced Debugging

### Debug 1: Check yt-dlp Format Selection
```python
import yt_dlp

# Test format selection directly
ydl_opts = {
    'listformats': True,
    'format': 'best[height>=1080][ext=mp4]'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.extract_info("YOUR_URL", download=False)
```

### Debug 2: Monitor Download Process
```bash
# Add verbose logging
export PYTHONPATH=$PYTHONPATH:.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from advanced_downloader import AdvancedYouTubeDownloader
downloader = AdvancedYouTubeDownloader()
downloader.download_with_best_quality('YOUR_URL', './debug_download', '1080p')
"
```

### Debug 3: Compare Multiple Strategies
```python
# Test all download strategies
from advanced_downloader import AdvancedYouTubeDownloader

downloader = AdvancedYouTubeDownloader()
strategies = [
    downloader._strategy_basic,
    downloader._strategy_with_cookies, 
    downloader._strategy_with_proxy_headers
]

for i, strategy in enumerate(strategies):
    try:
        result = strategy("YOUR_URL", download=False)
        if result:
            formats = result.get('formats', [])
            hd_formats = [f for f in formats if f.get('height', 0) >= 720]
            print(f"Strategy {i+1}: {len(hd_formats)} HD formats available")
    except Exception as e:
        print(f"Strategy {i+1} failed: {e}")
```

## 📊 Quality Benchmarks

### Minimum Kualitas HD:
- **720p HD**: Minimal 2.5 Mbps bitrate
- **1080p FHD**: Minimal 5 Mbps bitrate  
- **1440p 2K**: Minimal 9 Mbps bitrate
- **2160p 4K**: Minimal 15 Mbps bitrate

### File Size Estimates:
- **720p (5 min video)**: ~100-200 MB
- **1080p (5 min video)**: ~200-400 MB
- **1440p (5 min video)**: ~400-800 MB
- **4K (5 min video)**: ~800+ MB

### Codec Quality Ranking:
1. **H.264/AVC1** - Best compatibility, good quality
2. **VP9** - Better compression, newer
3. **AV1** - Best compression, limited support

## 🆘 Jika Semua Gagal

### Langkah Terakhir:
1. **Cek Video di Browser** - Pastikan video memang tersedia dalam HD di YouTube
2. **Test Video Lain** - Pastikan bukan masalah sistem
3. **Update yt-dlp** - `pip install --upgrade yt-dlp`
4. **Restart Server** - Restart aplikasi downloader
5. **Check FFmpeg** - Pastikan FFmpeg terinstall dengan benar

### Video Tidak Bisa HD:
Beberapa video memang dibatasi YouTube:
- Video lama (sebelum 2009)
- Video dengan copyright claim
- Video yang di-upload dalam resolusi rendah
- Video dengan geographical restrictions

### Contacts & Support:
Jika masih bermasalah, jalankan diagnostic tools:
```bash
python quality_analyzer.py "YOUR_URL"
python test_quality_verification.py
```

Dan bagikan output untuk analisis lebih lanjut.
