from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
# from airflow_dbt.operators.dbt_operator import DbtRunOperator, DbtTestOperator


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


(
    scrape_audiophile_data
)
