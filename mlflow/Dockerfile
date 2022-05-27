FROM conda/miniconda3:latest

RUN mkdir -p /mlflow/mlruns

WORKDIR /mlflow

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev

RUN pip install -U pip && \
    pip install psycopg2 mlflow boto3 mlflow-torchserve

CMD mlflow server \
    --backend-store-uri $DB_URI \
    --host 0.0.0.0 \
    --port $VIRTUAL_PORT \
    --default-artifact-root $FTP_URI 

