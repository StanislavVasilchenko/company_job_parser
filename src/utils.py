from config import config
import psycopg2


def create_database(db_name="employers_vacancies"):
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
    conn.close
