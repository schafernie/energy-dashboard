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
    

dag = DAG(
    'loading_data_from_smard',
    default_args=default_args,
    description='Load the data from smard and insert to postgres.',
    start_date=datetime(2026,8,21), 
    schedule='*/5 * * * *',
    catchup=False,   
)


loading_task = PythonOperator(
    task_id='run_loading_from_smard_script',
    python_callable=run_loading_from_smard_script,
    dag=dag,
) 

