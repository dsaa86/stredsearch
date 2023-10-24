#!/bin/sh

until cd /app/stredsearch
do
    echo "Waiting for server volume..."
done

celery -A stredsearch worker --loglevel=info --concurrency 1 -E

# celery --app stredsearch.celery.app worker