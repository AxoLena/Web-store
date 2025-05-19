FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN apt-get update && apt-get -qy install gcc libjpeg-dev libxslt-dev libpq-dev  \
    cron flake8 locales vim wget ca-certificates postgresql postgresql-contrib musl-dev

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt


COPY . .

RUN chmod 777 ./

