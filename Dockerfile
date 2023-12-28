FROM python:3.9.6-alpine
RUN pip install --upgrade pip
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
