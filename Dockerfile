FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD requirements.txt /code/
ADD scripts/development/docker-entrypoint.sh /usr/local/bin/

RUN pip install -r requirements.txt &&\
    chmod +x /usr/local/bin/docker-entrypoint.sh

COPY . /code/
EXPOSE 8000
CMD ["sh", "scripts/production/deploy.sh"]