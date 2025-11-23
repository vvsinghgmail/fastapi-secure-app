FROM python:3.12-slim

WORKDIR /app

# Install build tools for psycopg2 etc.
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY scripts ./scripts

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
