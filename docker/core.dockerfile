FROM python:3.12.0-alpine

WORKDIR /app

COPY core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core .
