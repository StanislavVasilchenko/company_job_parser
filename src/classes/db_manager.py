import psycopg2


class DBManager:
    def __init__(self, params: dict):
        self.params = params
        self.con = psycopg2.connect(**self.params)
        self.cur = self.con.cursor()

    def get_companies_and_vacancies_count(self) -> tuple:
        """Получает список всех компаний и количество вакансий у каждой компании."""

        rows_name = ["Название компании", "Кол-во вакансий"]

        self.cur.execute("""select employer_name, count(vacancy_id) as number_of_vacancies from vacancy
                                join employers using (employer_id)
                                group by employer_name""")

        data = self.cur.fetchall()
        return f"csv_files/{self.get_companies_and_vacancies_count.__name__}.csv", data, rows_name

    def get_all_vacancies(self) -> tuple:
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""

        rows_name = ["Название компании", "Вакансия", "ЗП от", "ЗП до", "Ссылка на вакансию"]

        self.cur.execute("""select employer_name, vacancy_name, salary_from, salary_to, url from vacancy
                            join employers using(employer_id)""")
        data = self.cur.fetchall()
        return f"csv_files/{self.get_all_vacancies.__name__}.csv", data, rows_name

    def get_avg_salary(self) -> tuple:
        """Получает среднюю зарплату по вакансиям."""

        rows_name = ["Средняя зарплата от", "Средняя зарплата до"]

        self.cur.execute("""select avg(salary_from), avg(salary_to) from vacancy""")
        data = self.cur.fetchall()
        return f"csv_files/{self.get_avg_salary.__name__}.csv", data, rows_name

    def get_vacancies_with_higher_salary(self) -> tuple:
        """Получает список всех вакансий,
         у которых зарплата выше средней по всем вакансиям."""

        rows_name = ["Название вакансии", "Зарплата от", "Зарплата до", "Ссылка на вакансию"]

        self.cur.execute("""select vacancy_name, salary_from, salary_to, url from vacancy
                            where salary_from > (select avg(salary_from) from vacancy)
                            and salary_to > (select avg(salary_to) from vacancy)""")
        data = self.cur.fetchall()
        return f"csv_files/{self.get_vacancies_with_higher_salary.__name__}.csv", data, rows_name

    def get_vacancies_with_keyword(self, key_words: list[str]) -> tuple:
        """Получает список всех вакансий,
         в названии которых содержатся переданные в метод слова, например python."""

        rows_name = ["Название вакансии", "Город", "Требования к соискателю", "Зарплата от", "Зарплата до",
                     "Ссылка на вакансию"]
        data = []
        for word in key_words:
            self.cur.execute(f"""select vacancy_name, city, requirement, salary_from, salary_to, url
                                from vacancy
                                where requirement like '%{word}'
                                or requirement like '%{word}%'
                                or requirement like '{word}%'
                                """)
            data_request_from_db = self.cur.fetchall()
            data.extend(data_request_from_db)
        return f"csv_files/{self.get_vacancies_with_keyword.__name__}.csv", data, rows_name
