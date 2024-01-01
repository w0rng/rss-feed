FROM python:3.12.1-alpine

WORKDIR /app

COPY summarizer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY summarizer .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]