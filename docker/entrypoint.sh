#!/bin/bash
set -e

echo "Checking Redis availability..."
until nc -z redis 6379; do
  echo "Redis is unavailable - waiting..."
  sleep 1
done
echo "Redis is available!"

# Ensure the socket directory exists and has correct permissions
mkdir -p /run/gunicorn
chmod 710 /run/gunicorn

exec "$@"
