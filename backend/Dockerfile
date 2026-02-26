FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY appforge ./appforge
COPY .env ./.env

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "appforge.api:app", "--host", "0.0.0.0", "--port", "8000"]
