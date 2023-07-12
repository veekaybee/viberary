FROM bitnami/pytorch
USER root


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=~/.cache/pip  pip install -r requirements.txt
COPY . /viberary
COPY src/ /viberary

RUN mkdir /viberary/data; exit 0
RUN chmod 777 /viberary/data; exit 0
ENV TRANSFORMERS_CACHE=/viberary/data
ENV SENTENCE_TRANSFORMERS_HOME=/viberary/data
ENV PYTHONPATH "${PYTHONPATH}:/viberary/src"

WORKDIR /viberary/src

CMD python  /viberary/src/api/app.py
