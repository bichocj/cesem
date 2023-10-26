FROM python:3.8

EXPOSE 8000
ENV DockerHOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR $DockerHOME
COPY cesem/. .


RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

RUN apt-get update &&  apt-get install -y  locales &&  rm -r /var/lib/apt/lists/*

RUN sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN export LC_ALL=C
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libpq-dev \
    gcc \
    postgresql-client

RUN apt-get autoremove -y gcc

RUN chmod a+x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
