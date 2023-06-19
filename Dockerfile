FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

COPY . /code

CMD python /code/src/api.py