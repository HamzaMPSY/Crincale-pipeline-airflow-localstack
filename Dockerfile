FROM apache/airflow:2.8.0
COPY requirements.txt .
RUN pip install --no-cache-dir "apache-airflow==2.8.0" -r requirements.txt