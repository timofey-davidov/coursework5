import json

def get_data(filename: str) -> list:
    """Функция для открытия и чтения json-файла"""
    with open(filename) as file:
        data = json.load(file)
    file.close()
    return data

def get_employes(data: list) -> list:
    """Функция для формирования списка кортежей"""
    employers_list = list()
    for employer in data:
        employers_list.append((str(employer['id']), employer['title']))
    return employers_list

def get_answers(answer: str, data: list):
    """Функция для вывода информации пользователю"""
    match answer:
    # 1 ВАРИАНТ - Список всех компаний и количество вакасий у каждой компании
        case "1":
            company_number = 1
            for company in data:
                print(f"{company_number}. У компании {company[0].upper()} {company[1]} активных вакансий")
                company_number += 1
    # 2 ВАРИАНТ - Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        case "2":
            vacancy_number = 1
            for vacancy in data:
                print(f"{vacancy_number}. Компания: {vacancy[0]}, вакансия: {vacancy[1]}, зарплата: {vacancy[2]}, ссылка на вакансию: {vacancy[3]}")
                vacancy_number += 1
    # 3 ВАРИАНТ - Среднюю зарплата по вакансиям
        case "3":
            print(f"Средняя зарплата: {data[0]}")
    # 4 ВАРИАНТ - Список всех вакансий, у которых зарплата ВЫШЕ СРЕДНЕЙ по всем вакансиям
        case "4":
            vacancy_number = 1
            for vacancy in data:
                print(f"{vacancy_number}. Вакансия: {vacancy[1]}, зарплата {vacancy[3]}, ссылка на вакансию: {vacancy[5]}")
                vacancy_number += 1
    # 5 ВАРИАНТ - Список вакансий, в названии которых содержится некоторое слово, например, python
        case "5":
            vacancy_number = 1
            for vacancy in data:
                print(f"{vacancy_number}. Вакансия: {vacancy[1]}, зарплата {vacancy[3]}, ссылка на вакансию: {vacancy[5]}")
                vacancy_number += 1