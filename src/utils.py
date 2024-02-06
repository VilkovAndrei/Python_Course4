from src.api_classes import HeadHunterAPI, SuperJobAPI
from src.savers import JSONSaver


def user_interaction():
    vacancies_json = []

    keyword = input("Введите ключевое слово для фильтрации вакансий: ")

    """Создание экземпляров класса для работы с API сайтов с вакансиями"""
    hh = HeadHunterAPI(keyword)
    sj = SuperJobAPI(keyword)

    """Получение вакансий с разных платформ"""
    for api in (hh, sj):
        vacancies_json.extend(api.get_vacancies(pages_count=2))

    connector = JSONSaver(keyword=keyword)
    connector.insert(vacancies_json=vacancies_json)

    while True:
        user_command = input(
            "1 - Вывести список вакансий;\n"
            "2 - Отсортировать по минимальной зарплате и вывести top вакансий;\n"
            "3 - Отфильтровать по требованиям;\n"
            "4 - Удалить загруженные вакансии из json-файла;\n"
            "exit - для выхода.\n"
            ">>> "
        )
        if user_command.lower() == "exit":
            break
        elif user_command == "1":
            vacancies = connector.select()
        elif user_command == "2":
            vacancies = connector.sorted_by_salary()
        elif user_command == "3":
            key_word_req = input("Введите запрос по требованиям вакансий  >>> ")
            vacancies = connector.filtered_by_requirement(key_word_req)
        elif user_command == "4":
            connector.delete_info()
            continue
        else:
            print("Введенная команда не опознана!")
            continue
        try:
            number_vacancies = int(input("Введите количество выводимых вакансий или ноль, чтобы вывести все  >>> "))
        except ValueError:
            print("Неверно введено количество выводимых вакансий.\n Повторите ввод!")
            continue

        if vacancies:
            counter = 1
            for vacancy in vacancies:
                if counter > number_vacancies and number_vacancies:
                    break
                print(vacancy, end="\n")
                counter += 1
