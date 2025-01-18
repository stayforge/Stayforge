FROM python:3.13-slim AS stayforge

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY . .

CMD /bin/sh -c "HOST=${HOST:-0.0.0.0} PORT=${PORT:-80} uvicorn app:app --host $HOST --port $PORT --workers 4"
