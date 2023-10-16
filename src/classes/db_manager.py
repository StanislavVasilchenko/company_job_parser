import psycopg2
from src.utils import write_in_csv


class DBManager:
    def __init__(self, params: dict):
        self.params = params
        self.con = psycopg2.connect(**self.params)
        self.cur = self.con.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании.
        И записывает полученные данные в csv файл companies_and_vacancies_count.csv"""

        rows_name = ["Название компании", "Кол-во вакансий"]
        file_name = "csv_files/companies_and_vacancies_count.csv"

        self.cur.execute("""select employer_name, count(vacancy_id) as number_of_vacancies from vacancy
                                join employers using (employer_id)
                                group by employer_name""")

        write_in_csv(file_name, self.cur.fetchall(), rows_name)
        self.con.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий,
         у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий,
         в названии которых содержатся переданные в метод слова, например python."""
        pass
