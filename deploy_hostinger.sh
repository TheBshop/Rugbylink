#!/bin/bash
# Hostinger VPS Deployment Script for RugbyLink
# Run this script on your Hostinger VPS after initial setup

set -e

echo "🚀 Starting RugbyLink deployment on Hostinger VPS..."

# Configuration
APP_NAME="rugbylink"
APP_USER="rugbylink"
APP_DIR="/home/$APP_USER/$APP_NAME"
DOMAIN="yourdomain.com"  # Replace with your actual domain

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as the $APP_USER user."
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git supervisor ufw

# Setup PostgreSQL
print_status "Setting up PostgreSQL database..."
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw rugbylink_db; then
    sudo -u postgres createuser --createdb $APP_USER 2>/dev/null || true
    sudo -u postgres createdb rugbylink_db -O $APP_USER 2>/dev/null || true
    print_warning "Please set a password for the database user manually:"
    echo "sudo -u postgres psql -c \"ALTER USER $APP_USER PASSWORD 'your_secure_password';\""
fi

# Create application directory
print_status "Creating application directory..."
mkdir -p $APP_DIR
cd $APP_DIR

# Clone repository (if not already present)
if [ ! -d ".git" ]; then
    print_status "Please clone your repository manually:"
    echo "git clone https://github.com/yourusername/rugbylink.git $APP_DIR"
    echo "Then run this script again."
    exit 1
fi

# Create virtual environment
print_status "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment and install requirements
print_status "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    cat > .env << EOF
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN
DATABASE_URL=postgresql://$APP_USER:your_secure_password@localhost:5432/rugbylink_db
EOF
    print_warning "Please update the database password in .env file!"
fi

# Run Django management commands
print_status "Running Django migrations and collecting static files..."
python manage.py migrate --settings=web_django.settings_production
python manage.py collectstatic --noinput --settings=web_django.settings_production

# Create superuser (interactive)
print_status "Creating Django superuser..."
echo "Please create a superuser for Django admin:"
python manage.py createsuperuser --settings=web_django.settings_production

# Create systemd service file
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/rugbylink.service > /dev/null << EOF
[Unit]
Description=RugbyLink Django App
After=network.target

[Service]
Type=notify
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/gunicorn --bind unix:$APP_DIR/rugbylink.sock web_django.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
print_status "Enabling and starting RugbyLink service..."
sudo systemctl daemon-reload
sudo systemctl enable rugbylink
sudo systemctl start rugbylink

# Create Nginx configuration
print_status "Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/rugbylink > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    client_max_body_size 20M;
    
    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias $APP_DIR/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    location / {
        proxy_pass http://unix:$APP_DIR/rugbylink.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }
}
EOF

# Enable Nginx site
print_status "Enabling Nginx site..."
sudo ln -sf /etc/nginx/sites-available/rugbylink /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Setup firewall
print_status "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'

# Create backup script
print_status "Creating backup script..."
mkdir -p $APP_DIR/backups
cat > $APP_DIR/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/home/rugbylink/rugbylink"
pg_dump rugbylink_db > $APP_DIR/backups/backup_$DATE.sql
find $APP_DIR/backups/ -name "*.sql" -mtime +7 -delete
EOF
chmod +x $APP_DIR/backup.sh

# Add backup to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * $APP_DIR/backup.sh") | crontab -

print_status "✅ Deployment completed successfully!"
echo ""
print_warning "Next steps:"
echo "1. Update your domain DNS to point to this server's IP"
echo "2. Update the database password in $APP_DIR/.env"
echo "3. Install SSL certificate: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo "4. Test your site: http://$DOMAIN"
echo ""
print_status "Useful commands:"
echo "• Check service status: sudo systemctl status rugbylink"
echo "• View logs: sudo journalctl -u rugbylink -f"
echo "• Restart application: sudo systemctl restart rugbylink"
echo "• Update application: cd $APP_DIR && git pull && sudo systemctl restart rugbylink"