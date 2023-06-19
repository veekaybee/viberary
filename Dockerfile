FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

ENV FLASK_APP viberary.py
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV FLASK_DEBUG: 1


ADD . /app

CMD ["flask", "run", "--host=0.0.0.0"]
