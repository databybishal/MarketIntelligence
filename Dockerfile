FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs

RUN chmod +x /app/wait_for_mssql.sh 2>/dev/null || true

ENV PYTHONUNBUFFERED=1

VOLUME ["/app/logs"]

CMD ["python", "runner.py"]
