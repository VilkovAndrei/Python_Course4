from abc import abstractmethod, ABC
import os.path
import json
from config import ROOT_DIR
from src.vacancy import Vacancy


class JobProcessing(ABC):
    """Абстрактный класс для работы с файлом с вакансиями"""

    @abstractmethod
    def insert(self, *args):
        """Записывает информацию в файл"""
        pass

    @abstractmethod
    def select(self):
        """Открывает для чтения информацию из файла.
           Возвращает список объектов класса вакансий.
        """
        pass

    @abstractmethod
    def delete_info(self):
        """ Удаляет информацию о вакансиях из файла """
        pass


class JSONSaver(JobProcessing):
    """Класс для работы с json-файлом с вакансиями"""

    def __init__(self, keyword):
        self.filename = os.path.join(ROOT_DIR, "data", keyword.title() + ".json").replace('\\', '/')
        self.vacancies_json = []
        self.vacancies = []

    def insert(self, vacancies_json):
        """Записывает информацию в файл"""
        self.vacancies_json = vacancies_json

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.vacancies_json, file, indent=4, ensure_ascii=False)

    def select(self):
        """Открывает для чтения информацию из файла.
           Возвращает список объектов класса вакансий.
        """
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        if vacancies:
            return [Vacancy(**x) for x in vacancies]
        return []

    def sorted_by_salary(self):
        """Возвращает отсортированный по минимальной зарплате список объектов класса вакансий"""

        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        self.vacancies = [Vacancy(**x) for x in vacancies]
        self.vacancies.sort(reverse=True)

        return self.vacancies

    def delete_info(self):
        """Удаляет информацию в json-файле с вакансиями"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)
