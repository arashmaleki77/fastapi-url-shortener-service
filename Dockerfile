ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION} as base
LABEL MAINTAINER "Arash Maleki <arashmaleki77>"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY . /src/

RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt

ENTRYPOINT [ "./docker-init.sh" ]
