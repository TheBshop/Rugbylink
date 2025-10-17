# Deployment Guide - RugbyLink

This guide covers deploying RugbyLink to production environments.

## Production Checklist

### 1. Environment Variables
Create a `.env` file or set environment variables:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/database
```

### 2. Database Setup
For production, use PostgreSQL:
```bash
pip install psycopg2-binary
```

Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rugbylink_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Static Files
```bash
python manage.py collectstatic --noinput
```

### 4. Media Files
Ensure media files are served properly:
- Set up cloud storage (AWS S3, Google Cloud, etc.) for production
- Configure `MEDIA_URL` and `MEDIA_ROOT` appropriately

### 5. Security Settings
Update `settings.py` for production:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 6. Web Server Configuration

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/your/project/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Gunicorn Configuration
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 web_django.wsgi:application
```

### 7. Process Management
Use systemd or supervisor to manage the Django process:

#### systemd service file (`/etc/systemd/system/rugbylink.service`)
```ini
[Unit]
Description=RugbyLink Django App
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment=PATH=/path/to/your/project/venv/bin
ExecStart=/path/to/your/project/venv/bin/gunicorn --bind unix:/path/to/your/project/rugbylink.sock web_django.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### 8. SSL Certificate
Use Let's Encrypt for free SSL:
```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 9. Backup Strategy
Set up automated database backups:
```bash
# Daily backup script
pg_dump rugbylink_db > backup_$(date +%Y%m%d).sql
```

### 10. Monitoring
- Set up logging
- Monitor server resources
- Use tools like Sentry for error tracking

## Docker Deployment (Alternative)

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_django.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=rugbylink_db
      - POSTGRES_USER=rugbylink_user
      - POSTGRES_PASSWORD=your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
```

## Performance Optimization

1. **Database Optimization**
   - Use database indexes
   - Optimize queries
   - Use database connection pooling

2. **Caching**
   - Implement Redis for caching
   - Use Django's cache framework

3. **CDN**
   - Use CloudFlare or AWS CloudFront for static files

4. **Image Optimization**
   - Compress images
   - Use WebP format
   - Implement lazy loading

## Maintenance

1. **Regular Updates**
   - Keep Django and dependencies updated
   - Monitor security advisories

2. **Database Maintenance**
   - Regular backups
   - Database optimization

3. **Log Monitoring**
   - Set up log rotation
   - Monitor error logs

## Scaling Considerations

1. **Horizontal Scaling**
   - Multiple application servers
   - Load balancer configuration

2. **Database Scaling**
   - Read replicas
   - Database sharding (if needed)

3. **Microservices**
   - Consider breaking into microservices for large scale

## Support

For deployment issues, check:
- Django deployment documentation
- Server logs
- Database logs
- Nginx/Apache logs

