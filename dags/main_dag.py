from airflow import DAG
import os
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
# from airflow_dbt.operators.dbt_operator import DbtRunOperator, DbtTestOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

GOOGLE_CLOUD_CONN_ID = "google_cloud_conn"


schedule_interval = "@daily"
start_date = days_ago(1)
default_args = {"owner": "mpsy", "depends_on_past": False, "retries": 1}


with DAG(
    dag_id="audiophile_e2e_pipeline",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
) as dag:

    scrape_audiophile_data = BashOperator(
        task_id="scrape_audiophile_data",
        bash_command="python /opt/airflow/tasks/scraper_extract/scraper.py",
    )

    upload_headphones_csv_file = LocalFilesystemToGCSOperator(
        task_id="upload_headphones_csv_file",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        src=os.getenv('PATH_TO_HEADPHONE_FILE'),
        dst=os.getenv('DESTINATION_HEADPHONE_FILE'),
        bucket=os.getenv('BUCKET_NAME'),
    )

    upload_iems_csv_file = LocalFilesystemToGCSOperator(
        task_id="upload_iems_csv_file",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        src=os.getenv('PATH_TO_IEMS_FILE'),
        dst=os.getenv('DESTINATION_IEMS_FILE'),
        bucket=os.getenv('BUCKET_NAME'),
    )


(
    scrape_audiophile_data
    >> [upload_headphones_csv_file, upload_iems_csv_file]
)
