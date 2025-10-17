#!/bin/bash
# RugbyLink Management Script for Hostinger

APP_DIR="/home/rugbylink/rugbylink"
cd $APP_DIR

case "$1" in
    deploy)
        echo "🚀 Deploying RugbyLink..."
        git pull origin main
        source venv/bin/activate
        pip install -r requirements.txt
        python manage.py migrate --settings=web_django.settings_production
        python manage.py collectstatic --noinput --settings=web_django.settings_production
        sudo systemctl restart rugbylink
        echo "✅ Deployment complete!"
        ;;
    logs)
        echo "📋 Showing application logs..."
        sudo journalctl -u rugbylink -f
        ;;
    status)
        echo "📊 Service Status:"
        sudo systemctl status rugbylink --no-pager
        echo ""
        echo "🌐 Nginx Status:"
        sudo systemctl status nginx --no-pager
        echo ""
        echo "🗄️ Database Status:"
        sudo systemctl status postgresql --no-pager
        ;;
    restart)
        echo "🔄 Restarting services..."
        sudo systemctl restart rugbylink
        sudo systemctl restart nginx
        echo "✅ Services restarted!"
        ;;
    backup)
        echo "💾 Creating backup..."
        ./backup.sh
        echo "✅ Backup created!"
        ;;
    ssl)
        echo "🔒 Installing SSL certificate..."
        sudo certbot --nginx -d $2 -d www.$2
        ;;
    *)
        echo "RugbyLink Management Script"
        echo ""
        echo "Usage: $0 {deploy|logs|status|restart|backup|ssl domain.com}"
        echo ""
        echo "Commands:"
        echo "  deploy  - Pull latest code and restart"
        echo "  logs    - Show application logs"
        echo "  status  - Show service status"
        echo "  restart - Restart all services"
        echo "  backup  - Create database backup"
        echo "  ssl     - Install SSL certificate for domain"
        exit 1
        ;;
esac