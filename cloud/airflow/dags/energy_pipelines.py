from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from energy_lib import compute_minute_stats, compute_trends

default_args = {
    'owner': 'analitica_energetica',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG('stats_trends',
         default_args=default_args,
         schedule_interval=timedelta(minutes=1),
         catchup=False) as dag:

    stats = PythonOperator(
        task_id='compute_minute_stats',
        python_callable=compute_minute_stats,
        op_kwargs={'window_s': 60}
    )

    trends = PythonOperator(
        task_id='compute_trends',
        python_callable=compute_trends,
        op_kwargs={'periods': ['1h','1d','7d','30d']}
    )

    stats >> trends
