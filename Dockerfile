FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

ENV FLASK_APP src/api/

ADD src .

CMD ["flask", "run", "--host=0.0.0.0"]
