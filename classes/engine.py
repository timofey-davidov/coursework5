import requests


class HH:
    """Класс для получения вакансий от работодателя"""
    def __init__(self, employer_id):
        self.employer_id = employer_id
        self.URL = f"https://api.hh.ru/vacancies?employer_id={self.employer_id}"

    def params_per_page(self, page=0):
        """Функциядляхранения параметров при обращении к API"""
        self.params = {
            'area': 113,
            "page": page,
            "per_page": 10
        }
        return self.params

    def get_vacancies(self):
        """Функция получения айдишников вакансий указанного работодателя"""
        self.vacancies_list = list()
        # ограничимся 10 вакансиями на работодателя
        for page in range(0, 10):
            if len(self.vacancies_list) < 10:
                self.response = requests.get(self.URL, params=self.params_per_page(page))
                if str(self.response.status_code).startswith("4") or str(self.response.status_code).startswith("5"):
                    print("ВНИМАНИЕ! Возникла ошибка подключения! Обработаны не все данные!")
                for vacancy in self.response.json()["items"]:
                    self.vacancies_list.append(vacancy["id"])
        return self.vacancies_list

    def get_vacancy_info(self, vacancy_id):
        """Функция формирования информации по вакансии по ее айдишнику"""
        self.vacancy_url=f"https://api.hh.ru/vacancies/{vacancy_id}"
        self.response = requests.get(self.vacancy_url, params=self.params_per_page(0))
        if str(self.response.status_code).startswith("4") or str(self.response.status_code).startswith("5"):
            print("ВНИМАНИЕ! Возникла ошибка подключения! Обработаны не все данные!")
        return self.response.json()

    def get_info(self, vacancy: dict):
        """Метод, достающий нужую информацию из словаря"""
        info = {
            "vacancy_id": vacancy.get("id"),
            "vacancy_name": vacancy.get("name"),
            "salary": self.get_salary(vacancy),
            "date_published": self.get_date_published(vacancy.get("published_at")),
            "url": vacancy.get("alternate_url"),
            "vacancy_description": vacancy.get("description"),
            'employer_id': vacancy.get('employer').get('id')
        }
        return info

    def get_salary(self, current_salary: dict):
        """Метод для получения зарплаты для вывода пользователю"""
        if current_salary.get("salary") is not None:
            _from = current_salary["salary"]["from"]
            _to = current_salary["salary"]["to"]

            if (_from and _to) or (not _from and _to):
                return _to
            elif _from and not _to:
                return _from
        else:
            return 0

    def get_date_published(self, date: str):
        if date is not None:
            return date.split("T")[0]
        return None