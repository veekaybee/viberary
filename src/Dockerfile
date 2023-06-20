FROM python:3.10-slim-bookworm as builder

WORKDIR /src

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=~/.cache/pip  \
    pip install -r requirements.txt

COPY . /src

ENV FLASK_APP=app

EXPOSE 5000

WORKDIR /src/api

CMD ["python", "app.py", "--host=0.0.0.0"]




