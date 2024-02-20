FROM python:3.12-slim-bullseye

WORKDIR /app
COPY ./requirements.txt .

COPY . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "main:app", "-c", -b unix:/gunicorn_socket/socket"gunicorn_conf.py"]
