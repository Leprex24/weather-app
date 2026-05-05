# syntax=docker/dockerfile:1
FROM python:3.12-alpine AS builder
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-alpine
LABEL org.opencontainers.image.authors="Kacper Sawicki" \
org.opencontainers.image.title="Aplikacja pogodowa zad1" \
org.opencontainers.image.version="1.0.0"

WORKDIR /app

COPY --from=builder /install /usr/local

COPY main.py .
COPY templates/ templates/

RUN adduser -D uzytkownik
USER uzytkownik

ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 CMD wget -qO- http://127.0.0.1:8080/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "main:app"]