from config import config
import psycopg2


def create_database(params, db_name):
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
    conn.close


def create_tables(cur, params, db_name):
    cur.execute("""CREATE TABLE employers(
                    employer_id int,
                    employer_name varchar(100),
                    vacancies_url text
                    )
                """)
    cur.execute("""CREATE TABLE vacancy (
                    vacancy_id SERIAL ,
                    employer_id int,
                    vacancy_name varchar(100),
                    salary_from int,
                    salary_to int,
                    city varchar(100),
                    url text,
                    requirement text,
                    responsibility text,
                    schedule text)
        """)

def filling_out_the_employer_table(cur, employers_list: list[object]) -> None:
    for employer in employers_list:
        cur.execute("""INSERT INTO employers VALUES (%s, %s, %s)""",
                    (employer.employer_id,
                     employer.employer_name,
                     employer.vacancies_url)
                    )

def filling_out_the_vacancy_table(cur, vacancyes_list: list[object]) -> None:
    for vacancy in vacancyes_list:
        cur.execute("""INSERT INTO vacancy (employer_id, vacancy_name, salary_from,
                                            salary_to, city, url, requirement, responsibility,
                                            schedule) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (vacancy.employer_id,
                     vacancy.vacancy_name,
                     vacancy.salary_from,
                     vacancy.salary_to,
                     vacancy.city,
                     vacancy.url,
                     vacancy.requirement,
                     vacancy.responsibility,
                     vacancy.schedule)
                    )