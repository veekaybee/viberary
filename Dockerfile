FROM bitnami/pytorch
USER root


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get -y --no-install-recommends install \
    -y git

RUN --mount=type=cache,target=~/.cache/pip  pip install -r requirements.txt
COPY . /viberary
COPY src/ /viberary

RUN mkdir /viberary/data; exit 0
RUN chmod 777 /viberary/data; exit 0
ENV TRANSFORMERS_CACHE=/viberary/data
ENV SENTENCE_TRANSFORMERS_HOME=/viberary/data
ENV PYTHONPATH "${PYTHONPATH}:/viberary/src"
ENV WORKDIR=/viberary
WORKDIR $WORKDIR
RUN git init .

CMD python  /viberary/src/api/app.py
