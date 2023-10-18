import psycopg2
import os

from src.classes.employer import EmployersHH
from src.classes.vacanies import VacanciesFromEmployers
from src.utils import create_database, create_tables, filling_out_the_employer_table, filling_out_the_vacancy_table, \
    write_in_csv, user_interaction
from config import config
from src.classes.db_manager import DBManager


def main():
    companies_list, data_base_name = user_interaction()
    employers = EmployersHH(companies_list)
    vacancies = VacanciesFromEmployers(employers)
    params = config()
    create_database(params, data_base_name)
    print(f"База данных {data_base_name} создана")
    params.update({'dbname': data_base_name})

    conn = None
    try:
        with psycopg2.connect(**params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                create_tables(cur, params)
                print("Таблицы созданы")

                filling_out_the_employer_table(cur, employers.employers)
                print("Таблица employers заполнена")

                filling_out_the_vacancy_table(cur, vacancies.all_vac)
                print("Таблица vacancies заполнена")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    directory_name = "csv_files"
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    key_words = input("Введите ключевые слова для поиска в описании требований к вакансии через пробел- ").split()
    manager = DBManager(params)
    requests_to_db = [manager.get_companies_and_vacancies_count(), manager.get_all_vacancies(),
                      manager.get_avg_salary(), manager.get_vacancies_with_higher_salary(),
                      manager.get_vacancies_with_keyword(key_words)]
    for req in requests_to_db:
        write_in_csv(*req)
    manager.con.close()


if __name__ == '__main__':
    main()
