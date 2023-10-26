#!/bin/sh

# until cd stredsearch
# do 
#     echo "Waiting for server"
# done

until python /usr/src/manage.py makemigrations
do
    echo "Waiting for migrations"
    sleep 10
done

until python /usr/src/manage.py migrate
do
    echo "Waiting for DB"
    sleep 10
done

echo "RUNNING SERVER COMMAND"

python /usr/src/manage.py runserver 0.0.0.0:8000