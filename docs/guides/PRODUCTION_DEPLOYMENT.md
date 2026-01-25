# Production Deployment Guide

Complete guide for deploying DigitalChild API to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Manual Deployment](#manual-deployment)
5. [Nginx Configuration](#nginx-configuration)
6. [SSL/TLS Setup](#ssltls-setup)
7. [Monitoring & Logging](#monitoring--logging)
8. [Security Checklist](#security-checklist)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Docker** (recommended) or Python 3.12+
- **Redis** (for caching and rate limiting)
- **Nginx** (reverse proxy)
- **Certbot** (for Let's Encrypt SSL certificates)

### System Requirements

- **CPU**: 2+ cores
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 10GB+ for application and data
- **Network**: Public IP address and domain name

## Environment Setup

###1. Clone Repository

```bash
git clone https://github.com/MissCrispenCakes/DigitalChild.git
cd DigitalChild
```

### 2. Create Production Environment File

```bash
cp .env.example .env
```

Edit `.env` with production values:

```bash
# Flask configuration
FLASK_ENV=production
SECRET_KEY=your-very-secure-random-secret-key-here
DEBUG=False

# API authentication
API_KEYS=key1-production-value,key2-production-value,key3-production-value

# CORS origins (comma-separated)
CORS_ORIGINS=https://grimdata.org,https://littlerainbowrights.com

# Redis configuration
CACHE_TYPE=RedisCache
CACHE_REDIS_URL=redis://localhost:6379/0
RATELIMIT_STORAGE_URI=redis://localhost:6379/1

# Rate limiting
RATELIMIT_PUBLIC=100 per hour
RATELIMIT_AUTHENTICATED=1000 per hour

# Data paths (default values shown)
METADATA_FILE=data/metadata/metadata.json
SCORECARD_FILE=data/scorecard/scorecard_main.xlsx
TAGS_CONFIG_DIR=configs

# Logging
LOG_LEVEL=INFO
```

### 3. Generate Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use output as `SECRET_KEY` in `.env`

### 4. Generate API Keys

```bash
python -c "import secrets; print(','.join([secrets.token_urlsafe(32) for _ in range(3)]))"
```

Use output as `API_KEYS` in `.env`

## Docker Deployment

### Quick Start with Docker Compose

1. **Build and start services:**

```bash
docker-compose up -d
```

2. **Check service status:**

```bash
docker-compose ps
```

3. **View logs:**

```bash
docker-compose logs -f api
```

4. **Test API health:**

```bash
curl http://localhost:5000/api/health
```

### Custom Docker Build

```bash
# Build image
docker build -t digitalchild-api:latest .

# Run container
docker run -d \
  --name digitalchild-api \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/data:/app/data:ro \
  -v $(pwd)/configs:/app/configs:ro \
  digitalchild-api:latest
```

### Docker Management Commands

```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# View resource usage
docker stats

# Remove all containers and volumes
docker-compose down -v
```

## Manual Deployment

### 1. Install Dependencies

```bash
# Create virtual environment
python3.12 -m venv .LittleRainbow
source .LittleRainbow/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt -r api_requirements.txt
```

### 2. Install and Configure Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verify Redis
redis-cli ping  # Should return "PONG"
```

### 3. Install Gunicorn

```bash
pip install gunicorn
```

### 4. Create Systemd Service

Create `/etc/systemd/system/digitalchild-api.service`:

```ini
[Unit]
Description=DigitalChild API
After=network.target redis-server.service
Requires=redis-server.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/digitalchild
Environment="PATH=/opt/digitalchild/.LittleRainbow/bin"
EnvironmentFile=/opt/digitalchild/.env
ExecStart=/opt/digitalchild/.LittleRainbow/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:5000 \
    --access-logfile /var/log/digitalchild/access.log \
    --error-logfile /var/log/digitalchild/error.log \
    --log-level info \
    wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5. Enable and Start Service

```bash
# Create log directory
sudo mkdir -p /var/log/digitalchild
sudo chown www-data:www-data /var/log/digitalchild

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable digitalchild-api
sudo systemctl start digitalchild-api

# Check status
sudo systemctl status digitalchild-api
```

## Nginx Configuration

### 1. Install Nginx

```bash
sudo apt-get install nginx
```

### 2. Create Site Configuration

Create `/etc/nginx/sites-available/digitalchild`:

```nginx
upstream digitalchild_api {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name api.grimdata.org;

    # Let's Encrypt verification
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name api.grimdata.org;

    # SSL certificates (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/api.grimdata.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.grimdata.org/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # API proxy
    location /api/ {
        proxy_pass http://digitalchild_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check (no auth required)
    location = /api/health {
        proxy_pass http://digitalchild_api/api/health;
        access_log off;
    }
}
```

### 3. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/digitalchild /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

## SSL/TLS Setup

### Using Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d api.grimdata.org

# Test auto-renewal
sudo certbot renew --dry-run
```

Certbot will automatically configure Nginx with SSL.

### Using Custom Certificates

If using custom SSL certificates:

```bash
# Copy certificates
sudo cp your-cert.pem /etc/ssl/certs/digitalchild-cert.pem
sudo cp your-key.pem /etc/ssl/private/digitalchild-key.pem

# Set permissions
sudo chmod 644 /etc/ssl/certs/digitalchild-cert.pem
sudo chmod 600 /etc/ssl/private/digitalchild-key.pem
```

Update Nginx config with certificate paths.

## Monitoring & Logging

### Application Logs

```bash
# Systemd service logs
sudo journalctl -u digitalchild-api -f

# Application logs (if using file logging)
tail -f /var/log/digitalchild/access.log
tail -f /var/log/digitalchild/error.log
```

### Nginx Logs

```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Redis Monitoring

```bash
# Connect to Redis CLI
redis-cli

# Monitor commands
MONITOR

# Get info
INFO

# Check memory usage
MEMORY STATS
```

### Health Monitoring

Set up automated health checks:

```bash
# Add to crontab
*/5 * * * * curl -f http://localhost:5000/api/health || echo "API health check failed" | mail -s "DigitalChild API Alert" admin@example.com
```

### Performance Monitoring

Use tools like:
- **Prometheus** + **Grafana** for metrics
- **Sentry** for error tracking
- **New Relic** or **DataDog** for APM

## Security Checklist

### Pre-Deployment

- [ ] Generated secure `SECRET_KEY`
- [ ] Generated random `API_KEYS`
- [ ] Updated `CORS_ORIGINS` to allowed domains
- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Configured SSL/TLS certificates
- [ ] Enabled firewall (allow ports 80, 443, 22 only)
- [ ] Disabled root SSH login
- [ ] Set up automated backups

### Post-Deployment

- [ ] Test all endpoints with valid API keys
- [ ] Verify rate limiting works
- [ ] Check SSL certificate validity
- [ ] Review application logs for errors
- [ ] Test CORS headers
- [ ] Verify security headers (X-Frame-Options, etc.)
- [ ] Run security scan (e.g., OWASP ZAP)
- [ ] Document API keys securely

### Ongoing

- [ ] Monitor application logs daily
- [ ] Review access logs for suspicious activity
- [ ] Update dependencies monthly
- [ ] Rotate API keys quarterly
- [ ] Test backup restoration quarterly
- [ ] Renew SSL certificates (automated with Let's Encrypt)

## Troubleshooting

### API Not Starting

**Check logs:**
```bash
sudo journalctl -u digitalchild-api -n 100
```

**Common issues:**
- Missing `.env` file or invalid environment variables
- Port 5000 already in use
- Python dependencies not installed
- Data files (metadata.json, scorecard.xlsx) not found

### 502 Bad Gateway

**Causes:**
- API service not running
- Incorrect Nginx upstream configuration
- Firewall blocking internal connections

**Fix:**
```bash
# Check if API is running
curl http://localhost:5000/api/health

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Restart services
sudo systemctl restart digitalchild-api nginx
```

### Rate Limit Errors

**Symptoms:** Getting 429 errors frequently

**Fix:**
- Increase rate limits in `.env`
- Ensure authenticated requests use `X-API-Key` header
- Check Redis connection

### Redis Connection Errors

**Check Redis:**
```bash
redis-cli ping
```

**Restart Redis:**
```bash
sudo systemctl restart redis-server
```

### High Memory Usage

**Check resource usage:**
```bash
docker stats  # If using Docker
top  # System processes
```

**Solutions:**
- Reduce Gunicorn workers
- Adjust Redis memory limits
- Enable Redis eviction policy

## Performance Optimization

### Gunicorn Workers

Calculate optimal workers:
```
workers = (2 × CPU cores) + 1
```

Example for 4-core server:
```bash
gunicorn -w 9 -b 0.0.0.0:5000 wsgi:app
```

### Redis Configuration

Edit `/etc/redis/redis.conf`:
```
maxmemory 512mb
maxmemory-policy allkeys-lru
```

### Caching Strategy

- Document list: 5 minutes
- Document detail: 15 minutes
- Scorecard data: 1 hour
- Tag statistics: 1 hour

## Backup Strategy

### Data Files

```bash
# Backup script
#!/bin/bash
BACKUP_DIR=/backup/digitalchild
DATE=$(date +%Y%m%d_%H%M%S)

tar -czf $BACKUP_DIR/data_$DATE.tar.gz \
    data/metadata/metadata.json \
    data/scorecard/scorecard_main.xlsx \
    configs/

# Rotate old backups (keep last 30 days)
find $BACKUP_DIR -name "data_*.tar.gz" -mtime +30 -delete
```

### Database Backups

If using PostgreSQL in the future:
```bash
pg_dump digitalchild > backup_$(date +%Y%m%d).sql
```

### Environment Configuration

```bash
# Backup .env (store securely, not in version control)
cp .env .env.backup_$(date +%Y%m%d)
```

## Updating the Application

```bash
# 1. Pull latest code
git pull origin main

# 2. Activate virtual environment
source .LittleRainbow/bin/activate

# 3. Update dependencies
pip install -r requirements.txt -r api_requirements.txt

# 4. Run tests
pytest tests/api/ -v

# 5. Restart service
sudo systemctl restart digitalchild-api

# 6. Check health
curl https://api.grimdata.org/api/health
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/MissCrispenCakes/DigitalChild/issues
- Documentation: https://grimdata.org/api/
