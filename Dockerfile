FROM python:3.10

WORKDIR /app
COPY ./app /app

RUN pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "main:app"]