class Vacancy:
    """
    Класс вакансий
    """
    def __init__(self, employer, title, url, salary_from, salary_to, requirement):
        self.employer = employer
        self.title = title
        self.url = url
        self.requirement = requirement

        if salary_from:
            self.salary_from = salary_from
        else:
            self.salary_from = 0
        if salary_to:
            self.salary_to = salary_to
        else:
            self.salary_to = 0

    def __str__(self):
        return f"Работодатель: {self.employer}\n" \
               f"Вакансия: {self.title}\n" \
               f"Зарплата: от {self.salary_from} до {self.salary_to}\n" \
               f"Требования: {self.requirement}\n" \
               f"Ссылка: {self.url}\n"

    def __ge__(self, other):
        """ Возвращает True или False """
        return self.salary_from >= other.salary_from

    def __eq__(self, other):
        """ Возвращает True или False """
        return self.salary_from == other.salary_from

    def __ne__(self, other):
        """ Возвращает True или False """
        return self.salary_from != other.salary_from

    def __le__(self, other):
        """ Возвращает True или False """
        return self.salary_from <= other.salary_from

    def __lt__(self, other):
        """ Возвращает True или False """
        return self.salary_from < other.salary_from
