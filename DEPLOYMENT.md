# Deployment Guide

This guide covers deploying the Finance AI Bot to various platforms.

## Prerequisites

- Telegram Bot Token (from @BotFather)
- Google Gemini API Key
- PostgreSQL database
- Python 3.10+

## Local Deployment

### Standard Installation

```bash
# Clone repository
git clone https://github.com/jaloliddin1006/finance-ai-bot.git
cd finance-ai-bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Initialize database
aerich init -t config.database.TORTOISE_ORM
aerich init-db

# Run bot
python main.py
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

## VPS Deployment (Ubuntu/Debian)

### 1. Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv postgresql git

# Create user for bot
sudo useradd -m -s /bin/bash botuser
sudo su - botuser
```

### 2. Install Bot

```bash
# Clone repository
git clone https://github.com/jaloliddin1006/finance-ai-bot.git
cd finance-ai-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure PostgreSQL

```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE finance_bot;
CREATE USER botuser WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE finance_bot TO botuser;
\q
EOF
```

### 4. Configure Environment

```bash
# Copy and edit .env
cp .env.example .env
nano .env

# Set:
BOT_TOKEN=your_token
DB_HOST=localhost
DB_PASSWORD=secure_password
GEMINI_API_KEY=your_key
```

### 5. Initialize Database

```bash
aerich init -t config.database.TORTOISE_ORM
aerich init-db
```

### 6. Setup Systemd Service

```bash
sudo nano /etc/systemd/system/finance-bot.service
```

Add:

```ini
[Unit]
Description=Finance AI Bot
After=network.target postgresql.service

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/finance-ai-bot
Environment="PATH=/home/botuser/finance-ai-bot/venv/bin"
ExecStart=/home/botuser/finance-ai-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 7. Start Service

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable finance-bot
sudo systemctl start finance-bot

# Check status
sudo systemctl status finance-bot

# View logs
sudo journalctl -u finance-bot -f
```

## Cloud Platforms

### Heroku

1. **Create Heroku app:**

```bash
heroku create finance-ai-bot
```

2. **Add PostgreSQL addon:**

```bash
heroku addons:create heroku-postgresql:mini
```

3. **Configure environment:**

```bash
heroku config:set BOT_TOKEN=your_token
heroku config:set GEMINI_API_KEY=your_key
```

4. **Create Procfile:**

```
worker: python main.py
```

5. **Deploy:**

```bash
git push heroku main
```

### Railway

1. **Create new project** on [Railway](https://railway.app)

2. **Add PostgreSQL database**

3. **Deploy from GitHub:**
   - Connect repository
   - Set environment variables
   - Deploy

4. **Environment variables:**
   ```
   BOT_TOKEN=your_token
   GEMINI_API_KEY=your_key
   DB_HOST=postgres.railway.internal
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=from_railway
   DB_NAME=railway
   ```

### Render

1. **Create new Web Service** on [Render](https://render.com)

2. **Add PostgreSQL database**

3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

4. **Set environment variables** in dashboard

### DigitalOcean App Platform

1. **Create new App**

2. **Add PostgreSQL database**

3. **Configure:**
   - GitHub repository
   - Python environment
   - Environment variables

4. **Deploy**

## Docker Deployment

### Docker Hub

1. **Build image:**

```bash
docker build -t yourusername/finance-bot:latest .
```

2. **Push to Docker Hub:**

```bash
docker login
docker push yourusername/finance-bot:latest
```

3. **Deploy on server:**

```bash
docker pull yourusername/finance-bot:latest
docker run -d \
  --name finance-bot \
  --env-file .env \
  yourusername/finance-bot:latest
```

### Docker Compose Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  bot:
    image: yourusername/finance-bot:latest
    env_file: .env
    depends_on:
      - postgres
    restart: always

volumes:
  postgres_data:
```

Deploy:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Variables

Required for all deployments:

```env
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
DB_HOST=database_host
DB_PORT=5432
DB_USER=database_user
DB_PASSWORD=database_password
DB_NAME=database_name
DEBUG=False
```

## Database Migrations

After deploying, run migrations:

```bash
# On server
aerich upgrade

# With Docker
docker exec finance-bot aerich upgrade
```

## Monitoring

### Logs

**Systemd:**
```bash
sudo journalctl -u finance-bot -f
```

**Docker:**
```bash
docker logs -f finance-bot
```

**Docker Compose:**
```bash
docker-compose logs -f bot
```

### Health Check

Add to your bot:

```python
# In main.py
@dp.message(Command("health"))
async def health_check(message: Message):
    await message.answer("✅ Bot is running")
```

## Backup

### Database Backup

```bash
# Create backup
pg_dump -U botuser finance_bot > backup.sql

# Restore backup
psql -U botuser finance_bot < backup.sql
```

### With Docker:

```bash
# Backup
docker exec finance_bot_db pg_dump -U postgres finance_bot > backup.sql

# Restore
docker exec -i finance_bot_db psql -U postgres finance_bot < backup.sql
```

## Security Best Practices

1. **Use environment variables** for sensitive data
2. **Enable firewall:**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```
3. **Use SSL for database** connections
4. **Keep dependencies updated:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```
5. **Regular backups** of database
6. **Monitor logs** for errors
7. **Use strong passwords**

## Troubleshooting

### Bot Not Starting

```bash
# Check logs
sudo journalctl -u finance-bot -n 50

# Test configuration
python -c "from config import settings; print('OK')"

# Test database connection
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -h localhost -U botuser -d finance_bot
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R botuser:botuser /home/botuser/finance-ai-bot

# Fix permissions
chmod +x main.py
```

## Updating Deployment

```bash
# Pull latest changes
cd ~/finance-ai-bot
git pull

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Run migrations
aerich upgrade

# Restart service
sudo systemctl restart finance-bot
```

## Performance Optimization

1. **Use connection pooling** for database
2. **Enable caching** where appropriate
3. **Monitor resource usage:**
   ```bash
   htop
   df -h
   ```
4. **Optimize database** queries
5. **Use CDN** for static files if needed

## Scaling

For high traffic:

1. **Horizontal scaling:** Multiple bot instances
2. **Load balancing:** Nginx or HAProxy
3. **Database replication:** PostgreSQL replicas
4. **Redis caching:** For session data
5. **Message queue:** For async processing

## Support

For deployment issues:
- Check logs first
- Review this guide
- Open GitHub issue
- Contact maintainer

## Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Systemd Documentation](https://systemd.io/)
