FROM python:3.11.1 as builder

ARG DEBUG
WORKDIR /app

RUN pip install -U pip setuptools wheel pdm
COPY pyproject.toml pdm.lock ./


RUN mkdir __pypackages__ &&\
    pdm install $( [ "$DEBUG" = "True" ] && echo "--dev" || echo "--prod") --no-lock --no-editable

####################################################

FROM python:3.11.1-alpine

WORKDIR /app

COPY --from=builder /app/__pypackages__/3.11 /pkgs
ENV PYTHONPATH "${PYTHONPATH}:/pkgs/lib"
ENV PATH "${PATH}:/pkgs/bin"

COPY src /app
