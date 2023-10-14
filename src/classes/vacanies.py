import requests


class VacanciesFromEmployers:

    def __init__(self, employers: list):
        self.employers = employers
        self.params = {
            "page": 0,
            "per_page": 100,
            "text": "Python",
            "area": 1,
            "professional_role": '96'

        }
        self.url = "https://api.hh.ru/vacancies"
        self.all_vac = self.creation_of_vacancy_objects()

    def get_requests(self):
        response = requests.get(url=self.url, params=self.params)
        if response.status_code == 200:
            return response.json()
        raise ConnectionError

    def get_all_vacancies_from_employers(self) -> list[dict]:
        vac_employers = []
        for emp in self.employers:
            self.url = emp.vacancies_url
            pages = self.get_requests().get("page")
            for page in range(pages + 1):
                self.params["page"] = page
                response_vac = self.get_requests()
                vac_employers.extend(response_vac["items"])
            print(f"{emp.employer_name} - done")
        return vac_employers

    def get_format_vacancies_from_employers(self) -> list[dict]:
        vacancies = self.get_all_vacancies_from_employers()
        format_vacancies = []
        for vac in vacancies:
            format_vac = {
                "employer_id": int(vac["employer"]["id"]),
                "vacancy_name": vac["name"],
                "city": vac["area"]["name"],
                "url": vac["alternate_url"],
                "requirement": vac["snippet"]["requirement"],
                "responsibility": vac["snippet"]["responsibility"],
                "schedule": vac["schedule"]["name"]
            }
            format_vacancies.append(format_vac)
        return format_vacancies

    def creation_of_vacancy_objects(self) -> list[object]:
        vacancies_for_packaging = self.get_format_vacancies_from_employers()
        creation_of_vacancy = [Vacancy(**format_vac) for format_vac in vacancies_for_packaging]
        return creation_of_vacancy


class Vacancy:

    def __init__(self, employer_id: int, vacancy_name: str, city: str,
                 url: str, requirement: str,
                 responsibility: str, schedule: str):
        self.employer_id = employer_id
        self.vacancy_name = vacancy_name
        self.city = city
        self.url = url
        self.requirement = requirement
        self.responsibility = responsibility
        self.schedule = schedule

    def __repr__(self):
        return (f"Name - {self.vacancy_name}\n"
                f"City - {self.city}\n"
                f"URL - {self.url}\n")
