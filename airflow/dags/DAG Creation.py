import sys
sys.path.append('../CollegeFootball')
from airflow.models import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import timedelta
from cfbd_api import cfb_rankings
from cfbd_api import email_ranking_list

default_arguments = {'owner': 'jcoby6',
                     'email': 'jcoby6@gmail.com',
                     'start_date': datetime(2022, 11, 1)}

cfb_dag = DAG('cfb_workflow',
              default_args=default_arguments,
              schedule_interval=timedelta(minutes=1))

cfb_ranking = PythonOperator(
    task_id='generate_rankings',
    python_callable=cfb_rankings,
    dag=cfb_dag)

email_cfb_rankings = PythonOperator(
    task_id='email_ranking_list',
    python_callable=email_ranking_list,
    dag=cfb_dag)

cfb_ranking >> email_cfb_rankings
