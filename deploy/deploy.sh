#!/bin/bash
# MasterCS — Deploy / Update Script
# Run this after setup_server.sh, and every time you update the code
# Usage: bash deploy.sh

set -e
APP_DIR="/opt/mastercs"
REPO_URL="https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git"  # UPDATE THIS

echo "=============================="
echo "  Deploying MasterCS..."
echo "=============================="

# --- Pull latest code ---
if [ -d "$APP_DIR/.git" ]; then
  echo "[1/7] Pulling latest code..."
  cd "$APP_DIR"
  git pull origin main
else
  echo "[1/7] Cloning repository..."
  git clone "$REPO_URL" "$APP_DIR"
  cd "$APP_DIR"
fi

# --- Backend setup ---
echo "[2/7] Setting up backend..."
cd "$APP_DIR/backend"

if [ ! -d "venv" ]; then
  python3.11 -m venv venv
fi
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# --- Build frontend ---
echo "[3/7] Building frontend..."
cd "$APP_DIR/frontend"
npm ci --silent
npm run build

# --- Copy built frontend to nginx html dir ---
echo "[4/7] Installing frontend..."
sudo rm -rf /var/www/mastercs
sudo cp -r "$APP_DIR/frontend/dist" /var/www/mastercs
sudo chown -R www-data:www-data /var/www/mastercs

# --- Configure nginx ---
echo "[5/7] Configuring nginx..."
sudo cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/mastercs
sudo ln -sf /etc/nginx/sites-available/mastercs /etc/nginx/sites-enabled/mastercs
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# --- Configure systemd service ---
echo "[6/7] Setting up API service..."
sudo cp "$APP_DIR/deploy/mastercs-api.service" /etc/systemd/system/mastercs-api.service
sudo systemctl daemon-reload
sudo systemctl enable mastercs-api
sudo systemctl restart mastercs-api

# --- Run DB migrations ---
echo "[7/7] Running database setup..."
cd "$APP_DIR/backend"
source venv/bin/activate
python3 -c "from app.db.base import Base; from app.db.session import engine; Base.metadata.create_all(bind=engine); print('DB tables created')"

echo ""
echo "=============================="
echo "  Deployment complete!"
echo "  Check status: sudo systemctl status mastercs-api"
echo "  Check logs:   sudo journalctl -u mastercs-api -f"
echo "=============================="
