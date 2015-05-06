FROM ubuntu:trusty
MAINTAINER Benjamin Kampmann <ben@hackership.org>

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y python python-pip python-virtualenv gunicorn supervisor && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /app

ADD requirements.txt /app/requirements.txt
ADD app.py /app/app.py

RUN pip install -r /app/requirements.txt

ADD supervisor.conf /etc/supervisor/conf.d/flask.conf

EXPOSE 5000

CMD supervisord -n