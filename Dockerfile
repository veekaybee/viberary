FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

ENV PYTHONPATH=/app

COPY . .

CMD flask --app /app/src/api/api.py run