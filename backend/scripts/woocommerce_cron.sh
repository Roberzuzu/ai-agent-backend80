#!/bin/bash
# Cron job script for auto-processing WooCommerce products
# Runs the Python script with proper environment

# Set working directory
cd /app/backend

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Run the cron job
/usr/local/bin/python3 /app/backend/cron_auto_process.py

# Exit with script's exit code
exit $?
