import requests
from src.classes.employer import EmployersHH


class Vacancy:

    def __init__(self, employer_id: int, vacancy_name: str, city: str,
                 salary_from: int, salary_to: int,
                 currency: str, url: str, requirement: str,
                 responsibility: str, schedule: str):
        self.employer_id = employer_id
        self.vacancy_name = vacancy_name
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.url = url
        self.requirement = requirement
        self.responsibility = responsibility
        self.schedule = schedule

    def __repr__(self):
        return (f"Name - {self.vacancy_name}\n"
                f"City - {self.city}\n"
                f"salary_from - {self.salary_from}, salary_to - {self.salary_to}\n"
                f"URL - {self.url}")
