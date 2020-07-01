ARG PYTHON_VERSION=3.8.3-slim-buster

FROM python:$PYTHON_VERSION as rtdp-base

RUN adduser --system --no-create-home --disabled-login --disabled-password --group rtdp

ENV PYTHON_PATH=/opt/rtdp
WORKDIR /opt/rtdp


RUN chown rtdp:rtdp /opt/rtdp

RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache


RUN \
    apt-get update; \
    apt-get install -y --no-install-recommends gpg gpg-agent software-properties-common wget watch; \
    wget -qO - https://packages.confluent.io/deb/5.3/archive.key | apt-key add -; \
    add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/5.3 stable main"; \
    add-apt-repository "deb [arch=amd64] https://deb.debian.org/debian jessie main"; \
    apt-get purge -y --auto-remove gpg gpg-agent software-properties-common wget; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl librdkafka-dev libgflags-dev libsnappy-dev liblz4-dev zlib1g-dev libbz2-dev libzstd-dev librocksdb-dev libpq-dev gcc; \
    rm -rf /var/lib/apt/lists/*

COPY requirements-kafka.txt .
RUN \
    apt-get update; \
    apt-get install -y --no-install-recommends build-essential; \
    pip install -r requirements-kafka.txt; \
    apt-get purge -y --auto-remove build-essential; \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY . .
FROM rtdp-base as dev-rtdp
#CMD ["faust", "-L", "uvloop", "-A", "consumers.faust_consumer.app:APP", "worker", "-l", "info"]
