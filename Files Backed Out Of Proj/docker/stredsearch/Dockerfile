FROM python:3-bookworm

RUN apt-get update && apt-get -y install python3-dev gcc libc-dev
# RUN apt-get -y install python3-dev
# RUN apt-get -y install gcc
# RUN apt-get -y install libc-dev

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./stredsearch /app/stredsearch
ADD ./docker /app/docker

RUN chmod +x /app/docker/stredsearch/server-entrypoint.sh
RUN chmod +x /app/docker/stredsearch/worker-entrypoint.sh
