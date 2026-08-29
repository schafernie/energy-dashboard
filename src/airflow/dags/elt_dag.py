import subprocess
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}


def run_loading_from_smard_script():
    script_name = "/opt/airflow/loading/load_from_smard.py"
    result = subprocess.run(["python",script_name],
            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


def run_dbt_transformation():
    result = subprocess.run(
        [
            "dbt", "run",
            "--profiles-dir", "/opt/airflow/dbt_profiles",
            "--project-dir", "/opt/airflow/transform",
            "--full-refresh",
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise Exception(f"dbt run failed with error: {result.stderr}")
    else:
        print(result.stdout)

dag = DAG(
    'extract_load_and_transform',
    default_args=default_args,
    description='Load the data from smard, insert to postgres and transform with dbt.',
    start_date=datetime(2026,8,21), 
    schedule='0 * * * *',
    catchup=False
) 

load_task = PythonOperator(
    task_id='run_loading_from_smard_script',
    python_callable=run_loading_from_smard_script,
    dag=dag
)


transform_task = PythonOperator(
    task_id='dbt_run',
    python_callable=run_dbt_transformation,
    dag=dag
)

load_task >> transform_task
