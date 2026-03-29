# MasterCS — AWS EC2 Deployment Guide

## What You Need
- AWS account (you have this ✓)
- A domain name (optional — you can use EC2's public IP)
- Your SSH key pair from AWS

---

## Step 1: Launch EC2 Instance

1. Go to AWS Console → **EC2** → **Launch Instance**
2. Settings:
   - **Name**: `mastercs-server`
   - **AMI**: Ubuntu Server 22.04 LTS (free tier eligible)
   - **Instance type**: `t3.micro` (free tier)
   - **Key pair**: Create new → name it `mastercs-key` → download `.pem` file
   - **Security Group** (open these ports):
     - SSH: port 22 (your IP only)
     - HTTP: port 80 (anywhere 0.0.0.0/0)
     - HTTPS: port 443 (anywhere, for later)
3. **Storage**: 20 GB gp3 (free tier gives 30 GB)
4. Click **Launch Instance**

Move your key to a safe place:
```bash
mv ~/Downloads/mastercs-key.pem ~/.ssh/
chmod 400 ~/.ssh/mastercs-key.pem
```

---

## Step 2: Push Code to GitHub

```bash
# In your project directory on Mac
cd /Users/ratikarora/Desktop/Project
git remote add origin https://github.com/YOUR_USERNAME/mastercs.git
git push -u origin main
```

> Create the repo at https://github.com/new first (make it private!)

---

## Step 3: SSH Into Your Server

```bash
# Get your EC2 Public IP from AWS Console → Instances
ssh -i ~/.ssh/mastercs-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## Step 4: Run Setup Script (ONE TIME ONLY)

```bash
# On the EC2 server:
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/mastercs/main/deploy/setup_server.sh
bash setup_server.sh
```

**Save the DB password it prints!**

---

## Step 5: Update deploy.sh with Your Repo

Edit `/Users/ratikarora/Desktop/Project/deploy/deploy.sh`:
```
REPO_URL="https://github.com/YOUR_USERNAME/mastercs.git"
```
Push the update, then on EC2:

---

## Step 6: Create .env File on Server

```bash
# On EC2:
cp /opt/mastercs/deploy/.env.production /opt/mastercs/backend/.env
nano /opt/mastercs/backend/.env
```

Fill in:
```
DATABASE_URL=mysql+pymysql://mastercs_user:YOUR_DB_PASSWORD@localhost/mastercs
SECRET_KEY=$(openssl rand -hex 32)   # Generate and paste
DEBUG=false
```

---

## Step 7: Deploy

```bash
# On EC2:
cd /opt/mastercs
bash deploy/deploy.sh
```

---

## Step 8: Import Your Database

```bash
# On your LOCAL Mac:
bash deploy/export_db.sh ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## Step 9: Test It

Open browser: `http://YOUR_EC2_PUBLIC_IP`

---

## Useful Commands

```bash
# Check API is running
sudo systemctl status mastercs-api

# View live logs
sudo journalctl -u mastercs-api -f

# Restart API
sudo systemctl restart mastercs-api

# Check nginx
sudo nginx -t && sudo systemctl reload nginx

# Update app (after git push)
cd /opt/mastercs && git pull && bash deploy/deploy.sh
```

---

## Optional: Free Domain + HTTPS

1. Get free domain at https://freedns.afraid.org or https://duckdns.org
2. Point it to your EC2 IP
3. Install SSL:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.duckdns.org
```

---

## Cost Estimate (with your $111 credits)

| Service | Monthly Cost |
|---------|-------------|
| EC2 t3.micro (free tier) | ~$0-8/month |
| 20GB EBS storage | ~$1.60/month |
| Data transfer (1GB) | ~$0.09/month |
| **Total** | **~$2-10/month** |

Your $111 will last well beyond April 23 — even after free tier ends.
