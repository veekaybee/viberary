FROM bitnami/pytorch 
USER root


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=~/.cache/pip  pip install -r requirements.txt
COPY . /app
COPY src/ /app

RUN mkdir /app/data; exit 0
RUN chmod 777 /app/data; exit 0
ENV TRANSFORMERS_CACHE=/app/data
ENV SENTENCE_TRANSFORMERS_HOME=/app/data
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

WORKDIR /app/src

CMD python  /app/src/api/app.py






