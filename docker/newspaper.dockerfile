FROM python:3.13.0-alpine

WORKDIR /app

COPY newspaper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY newspaper .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]