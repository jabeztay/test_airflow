import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators.pg_operator import PostgresToPostgresOperator

with DAG(
    dag_id="postgres_operator_dag",
    start_date=datetime.datetime(2021, 8, 1),
    schedule_interval="0 5 * * *",
    catchup=True,
    max_active_runs=1,
) as dag:

    create_source_sales_table = PostgresOperator(
        task_id="create_source_sales_table",
        postgres_conn_id="source_db",
        sql="sql/table_sales.sql"
    )

    populate_source_sales_table = PostgresOperator(
        task_id="populate_sales_table",
        postgres_conn_id="source_db",
        sql="sql/generate_sales.sql",
    )

    create_sales_target_table = PostgresOperator(
        task_id="create_target_sales_table",
        postgres_conn_id="target_db",
        sql="sql/table_sales.sql"
    )

    extract_sales_data = PostgresToPostgresOperator(
        task_id="extract_sales_to_target",
        source_postgres_conn_id="source_db",
        target_postgres_conn_id="target_db",
        sql="sql/extract_sales.sql"
    )

    create_source_sales_table >> populate_source_sales_table >> create_sales_target_table >> extract_sales_data
