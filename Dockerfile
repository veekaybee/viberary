FROM bitnami/pytorch 

WORKDIR /app

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=~/.cache/pip  pip install -r requirements.txt
COPY . /app
COPY src/ /app

RUN mkdir /app/data; exit 0
RUN chmod 777 /app/data; exit 0
ENV TRANSFORMERS_CACHE=/app/data
ENV SENTENCE_TRANSFORMERS_HOME=/app/data


WORKDIR /app/src/api
ENTRYPOINT [ "python" ]
CMD ["app.py" ]




