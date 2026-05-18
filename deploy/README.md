# Deployment Runbook

This project is prepared for a first production deployment on a temporary-free AWS EC2 Ubuntu host with:

- host-installed MySQL
- host-installed Nginx
- Dockerized Flask app
- HTTPS via Let's Encrypt
- host-mounted persistence for uploads and resume files

## 1. Target host shape

- Ubuntu EC2 instance
- DNS record pointed to the instance public IP
- open inbound ports:
  - `22` for SSH
  - `80` for HTTP
  - `443` for HTTPS

## 2. Host packages

Install on the EC2 host:

- Docker Engine
- Docker Compose plugin
- Nginx
- MySQL Server
- Certbot
- Python `venv` only if you want a non-container fallback

Use:

- `deploy/scripts/bootstrap-ubuntu.sh`

## 3. Host directory layout

Create these directories on the server:

```bash
sudo mkdir -p /opt/ayush-portfolio
sudo mkdir -p /opt/ayush-portfolio/runtime-data/uploads/certs
sudo mkdir -p /opt/ayush-portfolio/runtime-data/resume
sudo mkdir -p /opt/ayush-portfolio/deploy/backups
```

The container mounts:

- `/opt/ayush-portfolio/runtime-data/uploads` -> `/app/static/uploads`
- `/opt/ayush-portfolio/runtime-data/resume` -> `/app/static/resume`

## 4. MySQL setup

Install MySQL on the host, not in Docker.

Create DB and user:

```sql
CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'portfolio_user'@'127.0.0.1' IDENTIFIED BY 'replace-password';
GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```

Use a production `DATABASE_URL` in `.env`:

```env
DATABASE_URL=mysql+pymysql://portfolio_user:replace-password@127.0.0.1:3306/portfolio_db
```

## 5. App deployment

Clone the repo onto the host:

```bash
cd /opt
sudo git clone <your-repo-url> ayush-portfolio
cd /opt/ayush-portfolio
```

Copy `.env.example` to `.env` and fill real values.

Then deploy:

```bash
sudo bash deploy/scripts/deploy-app.sh
```

That script will:

- ensure runtime directories exist
- build the Docker image
- start the app container
- run `flask db upgrade` inside the container

## 6. Nginx reverse proxy

Use:

- `deploy/nginx/portfolio.conf`

Copy it to:

```bash
sudo cp deploy/nginx/portfolio.conf /etc/nginx/sites-available/ayush-portfolio
sudo ln -s /etc/nginx/sites-available/ayush-portfolio /etc/nginx/sites-enabled/ayush-portfolio
sudo nginx -t
sudo systemctl reload nginx
```

Update:

- `server_name`
- certificate paths after certbot runs

## 7. HTTPS

First make sure HTTP works on your domain.

Then run:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

After certbot updates Nginx, verify renewal:

```bash
sudo certbot renew --dry-run
```

## 8. systemd service

Use:

- `deploy/systemd/portfolio.service`

Install:

```bash
sudo cp deploy/systemd/portfolio.service /etc/systemd/system/portfolio.service
sudo systemctl daemon-reload
sudo systemctl enable portfolio.service
sudo systemctl start portfolio.service
```

This service uses Docker Compose to keep the app container running across reboots.

## 9. Health checks

App health endpoint:

- `http://127.0.0.1:8000/healthz`

Public validation:

- open `/`
- open `/about`
- open `/projects`
- open `/admin/login`
- download resume
- verify uploaded cert preview images load

## 10. Backups

Use:

- `deploy/scripts/backup-mysql.sh`

Example cron:

```bash
0 3 * * * /opt/ayush-portfolio/deploy/scripts/backup-mysql.sh >> /var/log/portfolio-backup.log 2>&1
```

This creates timestamped dumps in:

- `/opt/ayush-portfolio/deploy/backups`

Recommended extra backup scope:

- `.env`
- Nginx site config
- uploaded files under `runtime-data/uploads`
- resume file under `runtime-data/resume`

## 11. Known limits

- AWS free use is temporary, not permanent
- MySQL and app share one host, so this is a single-failure-domain deployment
- uploads remain instance-bound; this is not durable object storage
- manual deploy is intentional for this phase; CI/CD is deferred
