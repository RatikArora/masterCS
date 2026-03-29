#!/bin/bash
# Export local MySQL database and push to EC2
# Run from your LOCAL Mac — updates EC2 with your current DB
# Usage: bash export_db.sh ubuntu@YOUR_EC2_IP

EC2_HOST="${1:-ubuntu@YOUR_EC2_PUBLIC_IP}"
DUMP_FILE="/tmp/mastercs_$(date +%Y%m%d_%H%M%S).sql"
KEY_FILE="~/.ssh/mastercs-key.pem"   # Update to your key file path

echo "Exporting local MySQL database..."
mysqldump -u root mastercs > "$DUMP_FILE"
echo "Dump created: $DUMP_FILE ($(du -sh $DUMP_FILE | cut -f1))"

echo "Uploading to EC2..."
scp -i "$KEY_FILE" "$DUMP_FILE" "$EC2_HOST:/tmp/mastercs_dump.sql"

echo "Importing on EC2..."
ssh -i "$KEY_FILE" "$EC2_HOST" "
  DB_PASSWORD=\$(grep DB_PASSWORD /tmp/db_creds.txt | cut -d' ' -f2)
  # If already deployed, get password from .env
  if [ -f /opt/mastercs/backend/.env ]; then
    DB_URL=\$(grep DATABASE_URL /opt/mastercs/backend/.env | cut -d'@' -f1)
    DB_PASSWORD=\$(echo \$DB_URL | sed 's/.*://g')
  fi
  mysql -u mastercs_user -p\"\$DB_PASSWORD\" mastercs < /tmp/mastercs_dump.sql
  echo 'Database imported successfully!'
  rm /tmp/mastercs_dump.sql
"

rm "$DUMP_FILE"
echo "Done! Database synced to EC2."
