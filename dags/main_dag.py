from airflow import DAG
import os
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
# from airflow_dbt.operators.dbt_operator import DbtRunOperator, DbtTestOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.empty import EmptyOperator

GOOGLE_CLOUD_CONN_ID = "google_cloud_conn"


schedule_interval = "@daily"
start_date = days_ago(1)
default_args = {"owner": "mpsy", "depends_on_past": False, "retries": 1}

DATASET_NAME = os.environ.get("BQ_DATASET_NAME")
HEADPHONES_TABLE_NAME = os.environ.get("BQ_HEADPHONES_TABLE_NAME")
IEMS_TABLE_NAME = os.environ.get("BQ_IEMS_TABLE_NAME")
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

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

    upload_bronze_headphones_csv_file = LocalFilesystemToGCSOperator(
        task_id="upload_bronze_headphones_csv_file",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        src=os.getenv('PATH_TO_BRONZE_HEADPHONE_FILE'),
        dst=os.getenv('DEST_BRONZE_HEADPHONE_FILE'),
        bucket=os.getenv('BUCKET_NAME'),
    )

    upload_bronze_iems_csv_file = LocalFilesystemToGCSOperator(
        task_id="upload_bronze_iems_csv_file",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        src=os.getenv('PATH_TO_BRONZE_IEMS_FILE'),
        dst=os.getenv('DEST_BRONZE_IEMS_FILE'),
        bucket=os.getenv('BUCKET_NAME'),
    )

    sanitize_audiophile_data = BashOperator(
        task_id="sanitize_audiophile_data",
        bash_command="python /opt/airflow/tasks/validate_data/validate_sanitize_bronze.py",
    )

    upload_silver_headphones_csv_file = LocalFilesystemToGCSOperator(
        task_id="upload_silver_headphones_csv_file",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        src=os.getenv('PATH_TO_SILVER_HEADPHONE_FILE'),
        dst=os.getenv('DEST_SILVER_HEADPHONE_FILE'),
        bucket=os.getenv('BUCKET_NAME'),
    )

    upload_silver_iems_csv_file = LocalFilesystemToGCSOperator(
        task_id="upload_silver_iems_csv_file",
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
        src=os.getenv('PATH_TO_SILVER_IEMS_FILE'),
        dst=os.getenv('DEST_SILVER_IEMS_FILE'),
        bucket=os.getenv('BUCKET_NAME'),
    )
    # In the first place i was creating the big query dataset using airflow.
    # Then i remembred that i use terraform to interact with gcp
    # rip this working code
    # create_bq_dataset = BigQueryCreateEmptyDatasetOperator(
    #     task_id='create_bq_dataset',
    #     dataset_id=DATASET_NAME,
    #     gcp_conn_id=GOOGLE_CLOUD_CONN_ID,
    #     if_exists='ignore'
    # )
    empty_task_1 = EmptyOperator(
        task_id='empty_task_1',
        dag=dag
    )
    # Import tables from Cloud Storage
    import_headphones_table_to_bq = GCSToBigQueryOperator(
        task_id='import_headphones_table_to_bq',
        bucket=os.getenv('BUCKET_NAME'),
        source_objects=os.getenv('DEST_SILVER_HEADPHONE_FILE'),
        destination_project_dataset_table=f'{GOOGLE_CLOUD_PROJECT}:{DATASET_NAME}.{HEADPHONES_TABLE_NAME}',
        write_disposition='WRITE_TRUNCATE',
        autodetect=False,
        schema_fields=[
            {'name': 'rank', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'value_rating', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'model', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'price', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'signature', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'tone_grade', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'technical_grade', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'driver_type', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'fit_cup', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID
    )

    import_iems_table_to_bq = GCSToBigQueryOperator(
        task_id='import_iems_table_to_bq',
        bucket=os.getenv('BUCKET_NAME'),
        source_objects=os.getenv('DEST_SILVER_IEMS_FILE'),
        destination_project_dataset_table=f'{GOOGLE_CLOUD_PROJECT}:{DATASET_NAME}.{IEMS_TABLE_NAME}',
        write_disposition='WRITE_TRUNCATE',
        autodetect=False,
        schema_fields=[
            {'name': 'rank', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'value_rating', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'model', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'price', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'signature', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'tone_grade', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'technical_grade', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'driver_type', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        gcp_conn_id=GOOGLE_CLOUD_CONN_ID
    )

(
    scrape_audiophile_data >>
    [upload_bronze_headphones_csv_file, upload_bronze_iems_csv_file] >>
    sanitize_audiophile_data >>
    [upload_silver_headphones_csv_file, upload_silver_iems_csv_file] >> empty_task_1 >>
    [import_headphones_table_to_bq, import_iems_table_to_bq]
)
