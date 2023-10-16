import psycopg2
import csv


class DBManager:
    def __init__(self, params: dict):
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(**self.params)
        with conn.cursor() as cur:
            cur.execute("""select employer_name, count(vacancy_id) as number_of_vacancies from vacancy
                                join employers using (employer_id)
                                group by employer_name""")

            with open("companies_and_vacancies_count.csv", "w", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Название компании", "Кол-во вакансий"])
                writer.writerows(cur.fetchall())

        conn.close()

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