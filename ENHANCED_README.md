# 🎥 Enhanced YouTube Downloader - High Quality Edition

Sistem download YouTube yang telah ditingkatkan dengan fokus pada **kualitas asli** dan **pilihan resolusi lengkap**. Mendukung download video dengan kualitas setinggi mungkin sesuai yang tersedia di YouTube.

## ✨ Fitur Utama

### 🎯 Kualitas Video Terbaik
- **Resolusi Asli**: Download dalam resolusi hingga 4K (2160p) jika tersedia
- **Bitrate Optimal**: Mempertahankan bitrate video asli untuk kualitas terbaik
- **Format Specific**: Bisa memilih format ID spesifik untuk kontrol kualitas maksimal
- **Multiple Codecs**: Mendukung berbagai codec video (H.264, VP9, AV1)

### 🎵 Audio Berkualitas Tinggi
- **320 kbps MP3**: Audio dengan kualitas near-lossless
- **Multiple Audio Formats**: M4A, WebM, dan format audio berkualitas tinggi lainnya
- **Bitrate Selection**: Pilih bitrate audio sesuai kebutuhan (128, 192, 256, 320 kbps)

### 📊 Informasi Format Lengkap
- **Semua Resolusi Tersedia**: Lihat semua opsi dari 144p hingga 4K
- **Detail Bitrate**: Informasi bitrate video dan audio untuk setiap format
- **File Size Estimate**: Perkiraan ukuran file sebelum download
- **Codec Information**: Detail codec video dan audio yang digunakan

## 🔧 API Endpoints

### 1. **GET /** - Informasi API
```json
{
  "message": "Enhanced YouTube Downloader API",
  "version": "2.0.0",
  "features": [
    "High-quality video downloads",
    "Multiple resolution options", 
    "Detailed format information",
    "Audio quality selection",
    "Original quality preservation"
  ]
}
```

### 2. **POST /info** - Informasi Video Dasar
```bash
curl -X POST http://localhost:5000/info \
  -d "url=https://www.youtube.com/watch?v=VIDEO_ID"
```

**Response:**
```json
{
  "title": "Video Title",
  "duration": 300,
  "uploader": "Channel Name",
  "view_count": 1000000,
  "thumbnail": "https://...",
  "available_formats": [...]
}
```

### 3. **POST /formats** - Detail Format Lengkap ⭐
```bash
curl -X POST http://localhost:5000/formats \
  -d "url=https://www.youtube.com/watch?v=VIDEO_ID"
```

**Response:**
```json
{
  "title": "Video Title",
  "video_formats": [
    {
      "resolution": "2160p",
      "height": 2160,
      "width": 3840,
      "ext": "mp4",
      "vcodec": "avc1.640033",
      "tbr": 15000,
      "vbr": 13500,
      "fps": 30,
      "format_id": "137",
      "filesize": 125829120
    }
  ],
  "audio_formats": [
    {
      "quality": "320kbps",
      "abr": 320,
      "ext": "m4a",
      "acodec": "mp4a.40.2",
      "format_id": "140",
      "filesize": 12582912
    }
  ]
}
```

### 4. **POST /download** - Download dengan Kualitas Spesifik ⭐
```bash
# Download video 1080p dengan format ID spesifik
curl -X POST http://localhost:5000/download \
  -d "url=https://www.youtube.com/watch?v=VIDEO_ID" \
  -d "format=mp4" \
  -d "resolution=1080p" \
  -d "format_id=137" \
  --output video.mp4

# Download audio 320kbps
curl -X POST http://localhost:5000/download \
  -d "url=https://www.youtube.com/watch?v=VIDEO_ID" \
  -d "format=mp3" \
  -d "audio_quality=320" \
  --output audio.mp3
```

**Parameters:**
- `url` (required): YouTube video URL
- `format` (required): "mp4" atau "mp3"
- `resolution` (optional): "144p", "360p", "720p", "1080p", "1440p", "2160p"
- `format_id` (optional): ID format spesifik untuk kualitas terbaik
- `audio_quality` (optional): "128", "192", "256", "320"

## 🚀 Cara Menggunakan

### 1. Instalasi Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Server
```bash
python app.py
```

### 3. Buka Frontend
Akses `enhanced_frontend.html` di browser atau gunakan:
```bash
python -m http.server 8080
# Kemudian buka http://localhost:8080/enhanced_frontend.html
```

### 4. Test API
```bash
python test_enhanced_quality.py
```

## 🎯 Cara Mendapatkan Kualitas Terbaik

### 1. **Cek Format Tersedia Dulu**
```bash
curl -X POST http://localhost:5000/formats \
  -d "url=YOUR_YOUTUBE_URL"
```

### 2. **Pilih Format ID Terbaik**
Dari response `/formats`, pilih format dengan:
- **Resolusi tertinggi** (2160p > 1440p > 1080p > 720p)
- **Bitrate tertinggi** untuk resolusi yang sama
- **Codec terbaru** (AV1 > VP9 > H.264 untuk efisiensi)

### 3. **Download dengan Format ID**
```bash
curl -X POST http://localhost:5000/download \
  -d "url=YOUR_YOUTUBE_URL" \
  -d "format=mp4" \
  -d "format_id=FORMAT_ID_TERBAIK" \
  --output video_hq.mp4
```

## 📊 Contoh Kualitas yang Tersedia

### Video Formats
| Resolusi | Typical Bitrate | Use Case |
|----------|----------------|----------|
| 2160p (4K) | 15-45 Mbps | Kualitas cinema, layar besar |
| 1440p (2K) | 9-18 Mbps | Gaming, content creation |
| 1080p (FHD) | 5-8 Mbps | Standard HD, streaming |
| 720p (HD) | 2.5-5 Mbps | Mobile HD, bandwidth terbatas |
| 480p | 1-2.5 Mbps | Mobile standard |
| 360p | 0.5-1 Mbps | Low bandwidth |

### Audio Formats
| Quality | Bitrate | Use Case |
|---------|---------|----------|
| 320kbps | 320 kbps | Near-lossless, music production |
| 256kbps | 256 kbps | High quality listening |
| 192kbps | 192 kbps | Standard quality |
| 128kbps | 128 kbps | Basic quality, space saving |

## 🛠️ Troubleshooting Kualitas

### Video Tidak Ada Resolusi Tinggi?
1. **Video mungkin tidak di-upload dalam resolusi tinggi**
2. **Cek dengan `/formats` endpoint** untuk melihat resolusi maksimal
3. **Beberapa video lama** mungkin hanya tersedia hingga 720p

### Download Gagal?
1. **Video mungkin di-restrict** geografis atau age-gated
2. **Format ID mungkin tidak valid** - gunakan yang dari `/formats`
3. **Coba tanpa `format_id`** parameter, biarkan sistem pilih otomatis

### Kualitas Tidak Sesuai Harapan?
1. **Pastikan menggunakan `format_id`** dari format dengan bitrate tertinggi
2. **Kombinasi video+audio** akan di-merge untuk kualitas optimal
3. **Cek `tbr` (total bitrate)** di response `/formats`

## 🔄 Format Selection Logic

Sistem akan memilih kualitas terbaik dengan prioritas:

1. **Jika `format_id` disediakan**: Gunakan format exact tersebut
2. **Jika `resolution` disediakan**: Cari format terbaik untuk resolusi tersebut
3. **Default**: Pilih format terbaik yang tersedia

**Contoh selection untuk video:**
```
best[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[ext=mp4]+bestaudio/best[ext=mp4]/best
```

## 📝 Tips Menggunakan

### Untuk Kualitas Maksimal:
1. **Selalu gunakan `/formats` dulu** untuk melihat opsi
2. **Pilih format_id dengan bitrate tertinggi** untuk resolusi yang diinginkan  
3. **Untuk video 4K**, pastikan punya storage dan bandwidth cukup
4. **Untuk audio**, gunakan 320kbps jika ingin kualitas terbaik

### Untuk Efisiensi:
1. **1080p biasanya optimal** untuk kebanyakan kasus
2. **720p cocok untuk mobile** dan bandwidth terbatas
3. **192kbps audio sudah cukup** untuk listening biasa
4. **Gunakan `resolution` parameter** tanpa `format_id` untuk auto-selection

## 🆕 Perubahan dari Versi Sebelumnya

### ✅ Yang Ditambahkan:
- **Endpoint `/formats`** untuk detail format lengkap
- **Parameter `format_id`** untuk kontrol kualitas spesifik  
- **Parameter `audio_quality`** untuk pilihan bitrate audio
- **Enhanced format selection** dengan prioritas kualitas
- **Better error handling** dan logging
- **Frontend yang lebih canggih** dengan preview format

### 🔧 Yang Diperbaiki:
- **Video quality** sekarang menggunakan best available bitrate
- **Audio quality** default naik ke 320kbps dari 192kbps
- **Format merging** untuk kombinasi video+audio terbaik
- **More robust** error handling dan retry logic

---

**Nikmati download YouTube dengan kualitas terbaik! 🎉**

Jika ada masalah atau pertanyaan, cek log aplikasi atau jalankan test script untuk debugging.
