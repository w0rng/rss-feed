FROM python:3.12.2-alpine

WORKDIR /app

COPY telegram/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram .
CMD ["python", "main.py"]