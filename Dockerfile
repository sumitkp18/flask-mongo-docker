FROM python:3

WORKDIR  /app

ADD requirements.txt  /app/requirements.txt

RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

ENV  ENV_FILE_LOCATION ../.env

ADD .env /app

ADD flask_app /app/flask_app

EXPOSE 5000

CMD python /app/flask_app/app.py
