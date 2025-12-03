# Etapa 1: build
FROM python:3.11-alpine AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 2: execução
FROM python:3.11-alpine

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY . .

EXPOSE 5000
CMD ["python", "main.py"]
