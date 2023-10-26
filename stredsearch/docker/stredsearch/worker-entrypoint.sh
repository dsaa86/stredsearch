#!/bin/sh

until cd /app/stredsearch
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A stredsearch worker --loglevel=info --concurrency 1 -E
