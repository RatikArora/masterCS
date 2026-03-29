#!/bin/bash
# MasterCS — EC2 Ubuntu 22.04 Setup Script
# Run this ONCE on a fresh EC2 instance as ubuntu user
# Usage: bash setup_server.sh

set -e
echo "=============================="
echo "  MasterCS Server Setup"
echo "=============================="

# 1. System update
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y nginx python3.11 python3.11-venv python3-pip git unzip curl

# 3. Install MySQL 8.x
sudo apt install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# 4. Secure MySQL — set root password and create app DB
DB_PASSWORD=$(openssl rand -base64 24 | tr -d '/+=')
echo "Generated DB password: $DB_PASSWORD (save this!)"

sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$DB_PASSWORD';"
sudo mysql -u root -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS mastercs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -u root -p"$DB_PASSWORD" -e "CREATE USER IF NOT EXISTS 'mastercs_user'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
sudo mysql -u root -p"$DB_PASSWORD" -e "GRANT ALL PRIVILEGES ON mastercs.* TO 'mastercs_user'@'localhost'; FLUSH PRIVILEGES;"

echo "DB_URL=mysql+pymysql://mastercs_user:${DB_PASSWORD}@localhost/mastercs" > /tmp/db_creds.txt
echo "DB_PASSWORD: $DB_PASSWORD" >> /tmp/db_creds.txt
echo ">>> DB credentials saved to /tmp/db_creds.txt — copy them now!"

# 5. Create app directory
sudo mkdir -p /opt/mastercs
sudo chown -R ubuntu:ubuntu /opt/mastercs

# 6. Node.js 20 (for building frontend)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

echo ""
echo "=============================="
echo "  Setup complete!"
echo "  Next: run deploy.sh"
echo "=============================="
