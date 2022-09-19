"""
A test script to run a postgresql dag.
"""

# imports
import os
import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow import DAG
# create_pet_table, populate_pet_table, get_all_pets, and get_birth_date are
# examples of tasks created by
# instantiating the Postgres Operator

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "postgres_operator_dag"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    """create_pet_table = PostgresOperator(
        task_id="create_pet_table",
        sql="""
            # CREATE TABLE IF NOT EXISTS pet (
            # pet_id SERIAL PRIMARY KEY,
            # name VARCHAR NOT NULL,
            # pet_type VARCHAR NOT NULL,
            # birth_date DATE NOT NULL,
            # OWNER VARCHAR NOT NULL);
          # """,
    # )"""

    create_pet_table = PostgresOperator(
        task_id="create_pet_table",
        postgres_conn_id="postgres_default",
        sql="../sql/pet_schema.sql",
    )

    populate_pet_table = PostgresOperator(
        task_id="populate_pet_table",
        postgres_conn_id="postgres_default",
        sql="../sql/populate_pet_schema.sql",
    )

    get_all_pets = PostgresOperator(
        task_id="get_all_pets",
        postgres_conn_id="postgres_default",
        sql="SELECT * FROM pet;",
    )

    get_birth_date = PostgresOperator(
        task_id="get_birth_date",
        postgres_conn_id="postgres_default",
        sql="SELECT * FROM pet WHERE birth_date BETWEEN SYMMETRIC %(begin_date)s AND %(end_date)s",
        parameters={"begin_date": "2020-01-01", "end_date": "2020-12-31"},
    )

create_pet_table >> populate_pet_table >> get_all_pets >> get_birth_date
