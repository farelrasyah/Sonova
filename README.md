# YouTube Downloader API

Backend API Flask untuk mengkonversi tautan YouTube menjadi file MP3 atau MP4 dengan dukungan berbagai resolusi.

## Fitur

- ✅ Konversi YouTube ke MP3 (audio only)
- ✅ Konversi YouTube ke MP4 (video + audio)
- ✅ Dukungan multiple resolusi (140p, 240p, 360p, 480p, 720p, 1080p, 4K)
- ✅ Auto fallback ke kualitas terbaik yang tersedia
- ✅ CORS support untuk frontend
- ✅ Error handling yang comprehensive
- ✅ Logging untuk debugging
- ✅ Ready untuk deployment di server publik

## Teknologi

- **Python 3.12+**
- **Flask** - Web framework
- **yt-dlp** - YouTube downloader
- **ffmpeg** - Media processing (perlu diinstall terpisah)
- **Flask-CORS** - Cross-origin support

## Installation

1. Clone repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install ffmpeg:
   - Download dari https://ffmpeg.org/download.html
   - Extract dan tambahkan ke PATH

4. Jalankan aplikasi:
```bash
python app.py
```

## API Endpoints

### POST /download

Mengunduh video/audio dari YouTube dan mengembalikan file hasil.

**Request:**
```
Content-Type: multipart/form-data

url: string (required) - YouTube URL
format: string (required) - "mp3" atau "mp4" 
resolution: string (optional) - "140p", "240p", "360p", "480p", "720p", "1080p", "4k"
```

**Response:**
- Success: File download dengan proper Content-Type dan filename
- Error: JSON dengan pesan error

**Example:**
```bash
curl -X POST http://localhost:5000/download \
  -F "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -F "format=mp3"
```

## Environment Variables

Buat file `.env` untuk konfigurasi:

```
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
MAX_CONTENT_LENGTH=524288000  # 500MB
TEMP_FOLDER=./temp
```

## Deployment

Aplikasi ini dirancang untuk deployment di server publik dengan konfigurasi Cloudflare.

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)

```bash
docker build -t youtube-downloader-api .
docker run -p 5000:5000 youtube-downloader-api
```

## Error Handling

API mengembalikan error dalam format JSON:

```json
{
  "error": "Invalid YouTube URL",
  "details": "URL yang diberikan tidak valid atau tidak dapat diakses"
}
```

## Logging

Semua aktivitas dicatat dalam file `app.log` untuk debugging dan monitoring.
