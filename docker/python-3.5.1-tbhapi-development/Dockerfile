FROM tbhapi/python-3.5.1

ENV DOCKER_IMAGE=tbhapi/python-3.5.1-tbhapi-development

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main"    \
      > /etc/apt/sources.list.d/pgdg.list                                && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc |  \
      apt-key add -                                                      && \
    apt-get update                                                       && \
    apt-get install -y postgresql-server-dev-9.5

COPY tbh/ /home/user

RUN pip install --upgrade pip       && \
    pip install wheel               && \
    pip install -r requirements.txt && \
    python setup.py bdist_wheel && \
    python setup.py install

RUN mv gunicorn/app.conf /etc/init

# supervisor base configuration
COPY tbh/supervisor/supervisor.conf /etc/supervisor.conf
COPY tbh/supervisor/app.conf /etc/supervisor/conf.d/app.conf

# setup nginx
RUN mv nginx/app.conf /etc/nginx/nginx.conf
RUN service nginx stop

EXPOSE 80 8080

CMD ["supervisord", "-c", "/etc/supervisor.conf"]