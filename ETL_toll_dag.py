# import the libraries
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago  # Import days_ago

# Define DAG arguments
default_args = {
    'owner': 'Brown Ononiwu',
    'start_date': days_ago(0),  # Use days_ago to specify the start date
    'email': ['brown.ononiwu@gmail.com'],  # Corrected email format
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Project Tollgate',
    schedule_interval=timedelta(days=1),
)
unzip_data = BashOperator(
    task_id = 'unzip_data',
    bash_command = 'tar -xzvf /home/project/airflow/dags/finalassignment/tollgate.tgz',
    dag = dag
)

# Create a task to extract data from csv file 
extract = BashOperator( 
task_id='extract_data_from_csv', 
bash_command='cut -d"," -f1-4 /home/project/airflow/dags/finalassignment/vehicle-data.csv > /home/project/airflow/dags/finalassignment/csv_data.csv', dag=dag, ) 

# Create a BashOperator to run the extract_tsv_script 
extract_data_from_tsv = BashOperator( 
task_id='extract_data_from_tsv',
 bash_command='cut -d"\t" -f5-7 /home/project/airflow/dags/finalassignment/tollplaza-data.tsv | tr "\t" "," > /home/project/airflow/dags/finalassignment/tsv_data.csv', 
dag=dag, ) 

# Create a task to extract data from fixed width file 
extract_data_from_fixed_width = BashOperator( 
task_id='extract_data_from_fixed_width',
 bash_command='cut -d" " -f6-7 /home/project/airflow/dags/finalassignment/payment-data.txt | tr "\t" "," > /home/project/airflow/dags/finalassignment/fixed_width_data.csv', 
dag=dag,
 )
# Create a task to consolidate data extracted from previous tasks 
consolidate_data = BashOperator( 
task_id='consolidate_data', 
bash_command='paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv', 
dag=dag, 
)
# create a task to transform_data
transform_data = BashOperator(
    task_id='transform_data',
    bash_command="tr 'a-z' 'A-Z' < /home/project/airflow/dags/finalassignment/extracted_data.csv > /home/project/airflow/dags/finalassignment/transformed_data.csv",
    dag=dag,
)
# create pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
