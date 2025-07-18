# YouTube Downloader Troubleshooting Guide

## Masalah yang Sering Terjadi dan Solusinya

### 1. ❌ Error: "Could not establish connection. Receiving end does not exist"

**Penyebab:**
- Server Flask tidak berjalan
- Port 5000 sudah digunakan aplikasi lain
- Firewall memblokir koneksi
- CORS tidak dikonfigurasi dengan benar

**Solusi:**
1. Pastikan server berjalan:
   ```bash
   python app.py
   ```

2. Cek apakah port 5000 tersedia:
   ```bash
   netstat -an | findstr :5000
   ```

3. Jalankan auto-fix:
   ```bash
   python autofix.py
   ```

4. Jika masih bermasalah, coba port lain:
   ```bash
   set PORT=5001 && python app.py
   ```

### 2. ❌ Error: "Failed to fetch"

**Penyebab:**
- Timeout pada request
- Koneksi internet tidak stabil
- YouTube memblokir request
- File terlalu besar

**Solusi:**
1. Coba dengan resolusi yang lebih rendah
2. Restart aplikasi:
   ```bash
   Ctrl+C
   python app.py
   ```

3. Jalankan troubleshooting:
   ```bash
   python troubleshooting.py
   ```

4. Coba dengan URL yang berbeda

### 3. ❌ Download MP4 Kadang Berhasil, Kadang Tidak

**Penyebab:**
- YouTube menggunakan bot detection
- Format video tidak tersedia
- Koneksi timeout
- Temporary file cleanup prematur

**Solusi yang Sudah Diimplementasikan:**
1. **Enhanced Frontend dengan Retry Mechanism:**
   - Automatic retry up to 3 times
   - Exponential backoff
   - Better timeout handling (2 minutes per attempt)

2. **Improved Backend:**
   - Delayed cleanup (60 seconds)
   - Better CORS handling
   - Enhanced error messages

3. **Advanced Downloader:**
   - Increased retries (10 attempts)
   - Better timeout settings
   - Multiple bypass strategies

**Cara Penggunaan:**
1. Jalankan server:
   ```bash
   python app.py
   ```

2. Buka browser dan akses:
   ```
   file:///d:/Project%20Phyton%20Farel%20Rasyah/Sonova/test_frontend.html
   ```

3. Jika masih bermasalah, jalankan:
   ```bash
   python troubleshooting.py
   ```

### 4. ❌ FFmpeg Not Found

**Penyebab:**
- FFmpeg tidak terinstall
- FFmpeg tidak dalam PATH
- File FFmpeg corrupt

**Solusi:**
1. Jalankan setup FFmpeg:
   ```bash
   python setup_ffmpeg.py
   ```

2. Atau download manual dan extract ke folder `ffmpeg/`

3. Jalankan auto-fix:
   ```bash
   python autofix.py ffmpeg
   ```

### 5. ❌ Permission Denied

**Penyebab:**
- Folder temp tidak memiliki permission write
- File sedang digunakan aplikasi lain
- Antivirus memblokir

**Solusi:**
1. Jalankan as Administrator
2. Jalankan auto-fix:
   ```bash
   python autofix.py permissions
   ```

3. Tambahkan folder ke whitelist antivirus

### 6. ❌ Module Not Found

**Penyebab:**
- Python package tidak terinstall
- Virtual environment tidak aktif
- Python version tidak compatible

**Solusi:**
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan auto-fix:
   ```bash
   python autofix.py packages
   ```

3. Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```

## Tools yang Tersedia

### 1. Troubleshooting Tool
```bash
# Full diagnostic
python troubleshooting.py

# Test spesifik
python troubleshooting.py api
python troubleshooting.py ffmpeg
python troubleshooting.py youtube
python troubleshooting.py download
python troubleshooting.py temp
```

### 2. Auto-Fix Tool
```bash
# Fix semua masalah
python autofix.py

# Fix spesifik
python autofix.py temp
python autofix.py ffmpeg
python autofix.py cors
python autofix.py permissions
python autofix.py packages
python autofix.py network
```

### 3. Batch Scripts
```bash
# Windows troubleshooting
troubleshooting.bat

# Start server
start_enhanced_server.bat
```

## Tips Optimasi

### 1. Untuk Download yang Lebih Stabil:
- Gunakan resolusi yang lebih rendah untuk video panjang
- Pastikan koneksi internet stabil
- Restart aplikasi secara berkala
- Gunakan URL pendek (youtu.be format)

### 2. Untuk Performa yang Lebih Baik:
- Tutup aplikasi lain yang menggunakan bandwidth
- Gunakan SSD untuk folder temp
- Upgrade RAM jika memungkinkan
- Gunakan wired connection instead of WiFi

### 3. Untuk Troubleshooting yang Efektif:
- Jalankan troubleshooting.py secara berkala
- Check log file (app.log) untuk error details
- Monitor resource usage (CPU, RAM, Disk)
- Keep Python dan packages up to date

## Kontak dan Support

Jika masalah masih berlanjut:
1. Jalankan full diagnostic: `python troubleshooting.py`
2. Check app.log untuk error details
3. Coba dengan video yang berbeda
4. Restart komputer jika diperlukan

## Changelog Perbaikan

### Version 2.1.0 (Latest)
- ✅ Added retry mechanism dengan exponential backoff
- ✅ Improved timeout handling (2 minutes per attempt)
- ✅ Enhanced CORS configuration
- ✅ Delayed cleanup untuk mencegah file corruption
- ✅ Better error messages dan user feedback
- ✅ Added troubleshooting dan auto-fix tools
- ✅ Increased retry attempts (10x)
- ✅ Better socket timeout settings
- ✅ Enhanced download progress tracking

### Fitur Baru:
- 🔧 Automatic troubleshooting tool
- 🔧 Auto-fix untuk masalah umum
- 📊 Real-time diagnostic
- 🔄 Smart retry mechanism
- ⏰ Better timeout handling
- 🛡️ Enhanced error recovery
