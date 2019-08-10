FROM ubuntu:18.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get -y update \
  && apt-get install -y gettext python3.7 libpython3.7-dev python3-pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install pipenv
COPY Pipfile Pipfile.lock /app/
WORKDIR /app
# TODO: --dev needs to be removed
RUN pipenv install --system --deploy --dev

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

COPY . /app

RUN chown -R saleor:saleor /app/

EXPOSE 8000

CMD ["uwsgi", "--ini", "/app/shopozor/wsgi/uwsgi.ini"]
