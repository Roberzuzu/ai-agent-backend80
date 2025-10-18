#!/bin/bash
# Automated MongoDB backup cron job
# Add to crontab: 0 2 * * * /app/backend/scripts/backup_cron.sh

cd /app/backend
source .env

echo "=================================="
echo "Starting automated backup: $(date)"
echo "=================================="

python3 -m database.backup backup \
    --retention-days 7 \
    --max-backups 10 \
    >> /var/log/mongodb_backup.log 2>&1

echo "Backup completed: $(date)"
echo "=================================="
