FROM ubuntu:18.04

ARG ENABLE_DEV_TOOLS="true"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get -y update \
  && apt-get install -y gettext python3.7 libpython3.7-dev python3-pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN chmod u+x ./scripts/install/*.sh \
  && ./scripts/install/install.sh

RUN if [ "$ENABLE_DEV_TOOLS" == "true" ]; then ./scripts/install/install-dev.sh; fi

RUN groupadd -r saleor && useradd -r -g saleor saleor

RUN apt-get update \
  && apt-get install -y \
    libxml2 \
    libssl1.1 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    mime-support \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN chown -R saleor:saleor /app/

EXPOSE 8000

CMD ["uwsgi", "--ini", "/app/shopozor/wsgi/uwsgi.ini"]
