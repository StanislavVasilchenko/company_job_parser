from config import config
import psycopg2


def create_database(params, db_name):
    # params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
    conn.close


def create_tables(cur, params, db_name):
    cur.execute("""CREATE TABLE employers(
                    employer_id smallint,
                    employer_name varchar(50),
                    vacancies_url text
                    )
                """)
    cur.execute("""CREATE TABLE vacancy (
                    vacancy_id SERIAL,
                    employer_id smallint,
                    vacancy_name varchar(100),
                    salary_from smallint,
                    salary_to smallint,
                    city varchar(30),
                    url text,
                    requirement text,
                    responsibility text,
                    schedule text)
        """)