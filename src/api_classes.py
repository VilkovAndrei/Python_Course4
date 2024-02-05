from abc import abstractmethod, ABC
import time
import requests
from exceptions import ParsingError
from config import KeySuperJobAPI


class EngineAPI(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(EngineAPI):
    """Дочерний класс EngineAPI для HeadHunterAPI"""

    url = "https://api.hh.ru/vacancies/"

    def __init__(self, keyword, area=113):

        self.params = {
            "per_page": 10,
            "page": int,
            "text": keyword,
            "seach_field": "name",
            "only_with_salary": True,
            "area": area,
            "archived": False,
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()

    def get_vacancies(self, pages_count=10):
        count_vacancies = 0
        self.vacancies = []
        formatted_vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies["items"])
                print(f"Загружено вакансий: {len(page_vacancies)}")
                count_vacancies += len(page_vacancies)
            finally:
                time.sleep(0.4)
            if len(page_vacancies) == 0:
                break
        print(f"({self.__class__.__name__}) Загружено вакансий всего: {count_vacancies}")
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["employer"]["name"],
                "title": vacancy["name"],
                "url": vacancy["url"],
                "salary_from": vacancy["salary"]["from"] if vacancy["salary"] else None,
                "salary_to": vacancy["salary"]["to"] if vacancy["salary"] else None,
                "requirement": vacancy["snippet"]["requirement"],
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies


class SuperJobAPI(EngineAPI):
    """Дочерний класс EngineAPI для SuperJobAPI"""

    url = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.params = {
            "count": 10,
            "page": None,
            "keyword": keyword,
            "is_archive": False,
        }
        self.headers = {
            "X-Api-App-Id": KeySuperJobAPI
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["objects"]


    def get_vacancies(self, pages_count=10):
        count_vacancies = 0
        self.vacancies = []
        formatted_vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
                count_vacancies += len(page_vacancies)
            finally:
                time.sleep(0.4)
            if len(page_vacancies) == 0:
                break
        print(f"({self.__class__.__name__}) Загружено вакансий всего: {count_vacancies}")
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None,
                "requirement": vacancy["candidat"] if vacancy["candidat"] else "",
            }
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies
