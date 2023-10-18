from config import config
import psycopg2
import csv


def create_database(params, db_name) -> None:
    """Создает базу данных.
    Принимает параметры для подключения к БД и название БД
    """
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
    conn.close


def create_tables(cur, params) -> None:
    """Создает таблицы employers и vacancy в БД"""
    cur.execute("""CREATE TABLE employers(
                    employer_id int PRIMARY KEY ,
                    employer_name varchar(100),
                    vacancies_url text
                    )
                """)
    cur.execute("""CREATE TABLE vacancy (
                    vacancy_id SERIAL ,
                    employer_id int references employers(employer_id) ,
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
    """Заполняет таблицу employer данными. Принимает на вход список с объектами Employer"""
    for employer in employers_list:
        cur.execute("""INSERT INTO employers VALUES (%s, %s, %s)""",
                    (employer.employer_id,
                     employer.employer_name,
                     employer.vacancies_url)
                    )


def filling_out_the_vacancy_table(cur, vacancyes_list: list[object]) -> None:
    """Заполняет таблицу vacancy данными. Принимает на вход список с объектами Vacancy"""
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


def write_in_csv(name: str, data: list[tuple], rows_name: list[str]) -> None:
    """Записывает данные в csv файл"""
    with open(name, 'w', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(rows_name)
        writer.writerows(data)


def user_interaction() -> tuple:
    """Функция взаимодействия с пользователем"""
    companies_list = []
    while True:
        company_name = input("Введите название компании (По одной компании за раз) или q, quit для завершения ввода - ")
        match company_name:
            case ("q" | "quit"):
                break
            case str() as company if len(company) != 0:
                companies_list.append(company_name)
            case _:
                continue

    match companies_list:
        case list() as length if len(length) == 0:
            raise TypeError("Список работодателей не должен быть пустым")
    companies_list = list(set(companies_list))

    data_base_name = input("Введите название БД которую хотите создать - ")
    return companies_list, data_base_name
