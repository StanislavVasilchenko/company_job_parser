import requests


class EmployersHH:
    """Класс для получения данных о компаниях с сайта HH.ru"""
    BASE_URL = "https://api.hh.ru/employers"

    def __init__(self, company_name_list: list):
        self.verify_company_name_list(company_name_list)

        self.company_name_list = company_name_list
        self.params = {
            "text": None,
            "sort_by": "by_vacancies_open",
            "area": 1,
            "only_with_vacancies": True,
            "page": 0,
            'per_page': 100
        }
        self.employers = self.format_employers()

    def get_employers(self) -> list[dict]:
        """Подключается к сайту НН и получает данные о компаниях"""
        all_employers = []
        for company_name in self.company_name_list:
            self.params["text"] = company_name
            response = requests.get(url=self.BASE_URL, params=self.params).json()
            all_employers.extend(response["items"])
        return all_employers

    def format_employers(self) -> list[object]:
        """Преобразует данные о работодателе в вид:
        employer_id - id работодателя,
        employer_name - название компании,
        vacancies_url - ссылка на все открытые вакансии работодателя.
        Возвращает список с объектами Employer
        """
        format_employers_list = []
        employers = self.get_employers()
        for employer in employers:
            format_employer = {
                'employer_id': int(employer['id']),
                'employer_name': employer['name'],
                'vacancies_url': employer['vacancies_url']
            }
            format_employers_list.append(Employer(**format_employer))
        return format_employers_list

    @classmethod
    def verify_company_name_list(cls, company_name_list):
        """Проверяет что бы company_name_list не был пустым"""
        if not company_name_list:
            raise TypeError("Список работодателей не должен быть пустым")

    def __len__(self):
        return len(self.employers)

    def __repr__(self):
        return f"{self.employers}"

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        self.index += 1
        if self.index < len(self.employers):
            value = self.employers[self.index]
            return value
        else:
            raise StopIteration


class Employer:
    """Класс представления компании
    employer_id - id компании согласно сайта HH.ru,
    employer_name - название компании,
    vacancies_url - ссылка на все вакансии компании
    """

    def __init__(self, employer_id: int,
                 employer_name: str,
                 vacancies_url: str):
        self.employer_id = employer_id
        self.employer_name = employer_name
        self.vacancies_url = vacancies_url

    def __repr__(self):
        return (f"ID - {self.employer_id}\n"
                f"Company - {self.employer_name}\n"
                f"URL - {self.vacancies_url}")
