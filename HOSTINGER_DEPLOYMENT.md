# Hostinger Deployment Guide for RugbyLink

## Hostinger VPS Django Deployment

### Prerequisites
- Hostinger VPS plan (Business VPS or higher recommended)
- Domain name (can be purchased through Hostinger)
- Basic SSH knowledge

### Step 1: VPS Setup

1. **Purchase Hostinger VPS**
   - Go to Hostinger VPS plans
   - Choose Business VPS or higher (for better performance)
   - Select Ubuntu 22.04 LTS as OS

2. **Access VPS via SSH**
   ```bash
   ssh root@your-vps-ip
   ```

### Step 2: Server Setup

1. **Update system**
   ```bash
   apt update && apt upgrade -y
   ```

2. **Install required packages**
   ```bash
   apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git supervisor
   ```

3. **Create application user**
   ```bash
   adduser rugbylink
   usermod -aG sudo rugbylink
   su - rugbylink
   ```

### Step 3: Database Setup

1. **Configure PostgreSQL**
   ```bash
   sudo -u postgres createuser --interactive
   # Create user: rugbylink
   # Superuser: n
   # Create databases: y
   # Create roles: n
   
   sudo -u postgres createdb rugbylink_db -O rugbylink
   sudo -u postgres psql
   ALTER USER rugbylink PASSWORD 'your_secure_password';
   \q
   ```

### Step 4: Deploy Application

1. **Clone your repository**
   ```bash
   cd /home/rugbylink
   git clone https://github.com/yourusername/rugbylink.git
   cd rugbylink
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   nano .env
   ```
   Add your production settings:
   ```
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=postgresql://rugbylink:your_secure_password@localhost:5432/rugbylink_db
   ```

4. **Run migrations and collect static files**
   ```bash
   python manage.py migrate --settings=web_django.settings_production
   python manage.py collectstatic --noinput --settings=web_django.settings_production
   python manage.py createsuperuser --settings=web_django.settings_production
   ```

### Step 5: Gunicorn Setup

1. **Test Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:8000 web_django.wsgi:application
   ```

2. **Create Gunicorn service**
   ```bash
   sudo nano /etc/systemd/system/rugbylink.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=RugbyLink Django App
   After=network.target
   
   [Service]
   Type=notify
   User=rugbylink
   Group=rugbylink
   WorkingDirectory=/home/rugbylink/rugbylink
   Environment=PATH=/home/rugbylink/rugbylink/venv/bin
   EnvironmentFile=/home/rugbylink/rugbylink/.env
   ExecStart=/home/rugbylink/rugbylink/venv/bin/gunicorn --bind unix:/home/rugbylink/rugbylink/rugbylink.sock web_django.wsgi:application
   ExecReload=/bin/kill -s HUP $MAINPID
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start service**
   ```bash
   sudo systemctl enable rugbylink
   sudo systemctl start rugbylink
   sudo systemctl status rugbylink
   ```

### Step 6: Nginx Configuration

1. **Create Nginx config**
   ```bash
   sudo nano /etc/nginx/sites-available/rugbylink
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       client_max_body_size 20M;
       
       location /static/ {
           alias /home/rugbylink/rugbylink/staticfiles/;
           expires 30d;
           add_header Cache-Control "public, immutable";
       }
       
       location /media/ {
           alias /home/rugbylink/rugbylink/media/;
           expires 7d;
           add_header Cache-Control "public";
       }
       
       location / {
           proxy_pass http://unix:/home/rugbylink/rugbylink/rugbylink.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_redirect off;
       }
   }
   ```

2. **Enable site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/rugbylink /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Step 7: SSL Certificate (Free with Let's Encrypt)

1. **Install Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Get SSL certificate**
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

### Step 8: Domain Configuration

1. **In Hostinger Control Panel:**
   - Go to Domains → Manage
   - Update DNS records to point to your VPS IP
   - A record: @ → your-vps-ip
   - A record: www → your-vps-ip

### Step 9: Firewall Setup

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Step 10: Backup Setup

Create daily backup script:
```bash
nano /home/rugbylink/backup.sh
```

Add:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump rugbylink_db > /home/rugbylink/backups/backup_$DATE.sql
find /home/rugbylink/backups/ -name "*.sql" -mtime +7 -delete
```

```bash
chmod +x /home/rugbylink/backup.sh
mkdir /home/rugbylink/backups
crontab -e
# Add: 0 2 * * * /home/rugbylink/backup.sh
```

## Hostinger-Specific Tips

1. **VPS Plans**: Business VPS (4GB RAM) or higher recommended
2. **Location**: Choose server location closest to your target audience
3. **Monitoring**: Use Hostinger's VPS monitoring tools
4. **Support**: Hostinger has 24/7 support for VPS issues

## Cost Estimation
- Business VPS: ~$3.99/month (with discount)
- Domain: ~$8.99/year
- Total: ~$4-5/month

## Maintenance Commands

```bash
# Update application
cd /home/rugbylink/rugbylink
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=web_django.settings_production
python manage.py collectstatic --noinput --settings=web_django.settings_production
sudo systemctl restart rugbylink

# Check logs
sudo journalctl -u rugbylink -f
sudo tail -f /var/log/nginx/error.log

# Check services
sudo systemctl status rugbylink
sudo systemctl status nginx
sudo systemctl status postgresql
```

This setup will give you a professional, scalable Django deployment on Hostinger!