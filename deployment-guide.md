# commennt purposed to test github workflow @today
# haha testing again i think it will work.
# Deployment Guide for ET4D DMS on Windows VPS


This guide covers deploying the Django application on a Windows VPS with Nginx and NSSM.

## 1. Preparing the Application

First, ensure you have the application code on your VPS. Create and activate a virtual environment:

```powershell
# Navigate to your project folder
cd C:\path\to\DMS

# Create a virtual environment
python -m venv venv

# Activate the environment
.\venv\Scripts\Activate.ps1

# Install production dependencies
pip install -r requirements.txt
```

## 2. Django Production Settings

Create or update `.env` file in your project root with production settings:

```
DEBUG=False
SECRET_KEY=your_secure_secret_key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=sqlite:///C:/path/to/DMS/db.sqlite3
```

## 3. Collect Static Files

Run the collectstatic command to gather all static files:

```powershell
python manage.py collectstatic --noinput
```

## 4. Set Up Gunicorn with NSSM

Install NSSM if not already available:
1. Download from [NSSM website](https://nssm.cc/download)
2. Extract to a folder, e.g., `C:\nssm`
3. Add to PATH or use the full path in commands

Create a Windows service for your Django application:

```powershell
# Install the service (adjust paths as needed)
nssm install ET4D_DMS "C:\path\to\DMS\venv\Scripts\gunicorn.exe"
nssm set ET4D_DMS AppParameters "myproject.wsgi:application --bind 127.0.0.1:8001"
nssm set ET4D_DMS AppDirectory "C:\path\to\DMS"
nssm set ET4D_DMS AppEnvironmentExtra "PATH=C:\path\to\DMS\venv\Scripts;%PATH%"

# Set startup type to automatic
nssm set ET4D_DMS Start SERVICE_AUTO_START

# Set service display name and description
nssm set ET4D_DMS DisplayName "ET4D Dairy Management System"
nssm set ET4D_DMS Description "Django application for ET4D project"

# Start the service
nssm start ET4D_DMS
```

## 5. Configure Nginx

Add a new server block to your Nginx configuration (typically in `C:\nginx\conf\nginx.conf`):

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    access_log C:/nginx/logs/et4d_access.log;
    error_log C:/nginx/logs/et4d_error.log;

    # Static files
    location /static/ {
        alias C:/path/to/DMS/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # Media files (if applicable)
    location /media/ {
        alias C:/path/to/DMS/media/;
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

After editing the configuration, test and reload Nginx:

```powershell
# Test configuration
nginx -t

# Reload Nginx
nginx -s reload
```

## 6. Set Up Cloudflare Flexible SSL

1. Add your domain to Cloudflare
2. In DNS settings, point your domain to your VPS IP address
3. In SSL/TLS section:
   - Set SSL mode to "Flexible"
   - Enable "Always Use HTTPS" under Edge Certificates
4. Create a Page Rule:
   - URL pattern: `http://your-domain.com/*`
   - Setting: "Always Use HTTPS"

## 7. Automating Updates

Create a script for easy updates (`update.ps1`):

```powershell
# Change to project directory
cd C:\path\to\DMS

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Pull latest changes
git pull

# Install dependencies (if changed)
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Restart the service
nssm restart ET4D_DMS
```

## 8. Backup Strategy

Set up a scheduled task to backup your database and media files:

```powershell
# Create backup directory
$backupDir = "C:\backups\et4d"
New-Item -ItemType Directory -Force -Path $backupDir

# Backup database
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item "C:\path\to\DMS\db.sqlite3" -Destination "$backupDir\db_$timestamp.sqlite3"

# Backup media files (if applicable)
Compress-Archive -Path "C:\path\to\DMS\media" -DestinationPath "$backupDir\media_$timestamp.zip"

# Keep only last 7 backups
Get-ChildItem $backupDir -Filter "db_*.sqlite3" | Sort-Object LastWriteTime -Descending | Select-Object -Skip 7 | Remove-Item
Get-ChildItem $backupDir -Filter "media_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -Skip 7 | Remove-Item
```

Add this script to Windows Task Scheduler to run daily.

## Troubleshooting

- **Check service status**: `nssm status ET4D_DMS`
- **View application logs**: `Get-Content -Path "C:\path\to\DMS\logs\app.log" -Tail 50`
- **Check Nginx logs**: `C:\nginx\logs\et4d_error.log`
- **Restart service**: `nssm restart ET4D_DMS` 
