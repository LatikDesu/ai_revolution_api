#!/bin/sh

until cd /app/server
do
    echo "Waiting for server volume..."
done

/opt/venv/bin/celery -A src worker --loglevel=info --concurrency 5 -E
