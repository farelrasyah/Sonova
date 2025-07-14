# 🚀 Panduan Deployment YouTube Downloader API

## 📋 Persiapan Sebelum Deployment

### 1. Server Requirements
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+
- **Python**: 3.8+
- **Memory**: Minimal 2GB RAM (Recommended: 4GB+)
- **Storage**: Minimal 10GB free space
- **Network**: Port 5000 terbuka (atau port custom)

### 2. Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip ffmpeg nginx

# CentOS/RHEL
sudo yum install python3 python3-pip ffmpeg nginx

# Windows
# Download ffmpeg dari https://ffmpeg.org/download.html
# Install Python dari python.org
```

## 🛠️ Deployment Steps

### Method 1: Direct Deployment

1. **Clone/Upload project ke server**
```bash
git clone <your-repo-url>
cd youtube-downloader-api
```

2. **Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Environment**
```bash
cp .env.example .env
# Edit .env file dengan konfigurasi yang sesuai
```

5. **Test aplikasi**
```bash
python test_comprehensive.py
```

6. **Run Production Server**
```bash
gunicorn -c gunicorn.conf.py app:app
```

### Method 2: Docker Deployment

1. **Build Docker Image**
```bash
docker build -t youtube-downloader-api .
```

2. **Run Container**
```bash
docker run -d \
  --name youtube-api \
  -p 5000:5000 \
  -v ./temp:/app/temp \
  -v ./logs:/app/logs \
  youtube-downloader-api
```

3. **Using Docker Compose**
```bash
docker-compose up -d
```

### Method 3: Cloudflare Workers + Server

1. **Deploy API ke server** (Method 1 atau 2)

2. **Setup Cloudflare Worker**
```bash
# Edit cloudflare-worker.js
# Ganti BACKEND_URL dengan URL server Anda
# Deploy ke Cloudflare Workers
```

3. **Configure Domain**
```bash
# Setup custom domain di Cloudflare
# Configure SSL/TLS
```

## 🌐 Nginx Configuration

### /etc/nginx/sites-available/youtube-api
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
        
        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }
        
        # Increase timeout for large downloads
        proxy_connect_timeout       300;
        proxy_send_timeout          300;
        proxy_read_timeout          300;
        send_timeout                300;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

### Enable site
```bash
sudo ln -s /etc/nginx/sites-available/youtube-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 SSL/HTTPS Setup

### Using Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 🔧 Systemd Service (Linux)

### /etc/systemd/system/youtube-api.service
```ini
[Unit]
Description=YouTube Downloader API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/youtube-downloader-api
Environment=PATH=/path/to/youtube-downloader-api/venv/bin
ExecStart=/path/to/youtube-downloader-api/venv/bin/gunicorn -c gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always

[Install]
WantedBy=multi-user.target
```

### Enable service
```bash
sudo systemctl daemon-reload
sudo systemctl enable youtube-api
sudo systemctl start youtube-api
sudo systemctl status youtube-api
```

## 📊 Monitoring & Logging

### Log Files
- Application logs: `logs/app.log`
- Access logs: `logs/access.log`
- Error logs: `logs/error.log`

### Health Check
```bash
curl -f http://localhost:5000/
```

### Process Monitoring
```bash
# Check if service is running
sudo systemctl status youtube-api

# Check logs
sudo journalctl -u youtube-api -f

# Check resource usage
htop
```

## 🛡️ Security Considerations

### 1. Environment Variables
```bash
# .env file should contain:
SECRET_KEY=your-very-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False
```

### 2. Rate Limiting
- Implement rate limiting per IP
- Set download limits per user
- Monitor for abuse

### 3. Input Validation
- Validate all YouTube URLs
- Sanitize file names
- Check file sizes

### 4. Server Security
```bash
# Firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Updates
sudo apt update && sudo apt upgrade -y
```

## 🚀 Performance Optimization

### 1. Caching
```python
# Enable caching for video info
CACHE_TIMEOUT = 3600  # 1 hour
```

### 2. Resource Limits
```python
# gunicorn.conf.py
workers = 4
worker_connections = 1000
timeout = 300
max_requests = 1000
```

### 3. Database (Optional)
```python
# For storing download history/analytics
# Use Redis for caching
# Use PostgreSQL for persistent data
```

## 🧪 Testing Deployment

### 1. Health Check
```bash
curl -X GET http://yourdomain.com/
```

### 2. API Test
```bash
curl -X POST http://yourdomain.com/download \
  -F "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -F "format=mp3" \
  -o test.mp3
```

### 3. Load Testing
```bash
# Install apache bench
sudo apt install apache2-utils

# Test concurrent requests
ab -n 100 -c 10 http://yourdomain.com/
```

## 📱 Frontend Integration

### JavaScript Example
```javascript
const API_URL = 'https://yourdomain.com';

async function downloadVideo(url, format, resolution) {
    const formData = new FormData();
    formData.append('url', url);
    formData.append('format', format);
    if (resolution) formData.append('resolution', resolution);
    
    const response = await fetch(`${API_URL}/download`, {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `video.${format}`;
        a.click();
    }
}
```

## 🔍 Troubleshooting

### Common Issues

1. **FFmpeg not found**
```bash
which ffmpeg
sudo apt install ffmpeg
```

2. **Permission denied**
```bash
sudo chown -R www-data:www-data /path/to/app
sudo chmod -R 755 /path/to/app
```

3. **Port already in use**
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

4. **Memory issues**
```bash
# Increase swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Debug Mode
```bash
# Enable debug temporarily
export FLASK_DEBUG=True
python app.py
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Multiple instances behind load balancer
# Use Docker Swarm or Kubernetes
```

### Vertical Scaling
```bash
# Increase server resources
# Optimize gunicorn workers
# Use Redis for caching
```

## 📚 Additional Resources

- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.0.x/deploying/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Cloudflare Workers](https://workers.cloudflare.com/)
- [Docker Documentation](https://docs.docker.com/)

## 🆘 Support

Jika mengalami masalah:
1. Periksa log files
2. Jalankan test_comprehensive.py
3. Periksa status service systemd
4. Verify ffmpeg installation
5. Check network connectivity
