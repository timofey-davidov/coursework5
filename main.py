# блок импорта
from time import sleep
from classes.engine import HH
from classes.dbmanager import DBManager
from utils.utils import get_data, get_employes, get_answers
from utils.config import config

# блок глобальных переменных
DATABASE_PATH = 'database/employers_info.json'

# блок определения основной функции
def main():
    # достаем конфигурацию подключения к БД postgres
    db_configuration=config("utils/database.ini")
    # создаем объект для работы с БД
    db = DBManager('hh', db_configuration)
    # непосредственно создаем БД
    db.create_database()
    # получаем список работодателей из заранее подготовленного файла
    employees = get_data(DATABASE_PATH)
    # добавляем работодателей в БД
    for employer in employees:
        db.add_data("employees", employer)
        # создаем объект для работы с вакансиями
        employee = HH(employer["id"])
        # формируем список с айдишниками вакансий данного работодателя
        vacancies_list = employee.get_vacancies()
        sleep(0.25)
        for i in vacancies_list:
            # получаем содержимое (данные) вакансии
            data = employee.get_info(employee.get_vacancy_info(i))
            sleep(0.25)
            # добавляем вакансию в БД
            db.add_data("vacancies", data)
    print('База данных обновлена!')
    while True:
        print("Что вывести?")
        sleep(0.2)
        print(f"1. Список всех компаний и количество вакасий у каждой компании")
        sleep(0.2)
        print(f"2. Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
        sleep(0.2)
        print(f"3. Среднюю зарплата по вакансиям")
        sleep(0.2)
        print(f"4. Список всех вакансий, у которых зарплата ВЫШЕ СРЕДНЕЙ по всем вакансиям")
        sleep(0.2)
        print(f"5. Список вакансий, в названии которых содержится некоторое слово, например, python")
        sleep(0.2)
        user_input = input("Напишите свой вариант разборчивым подчероком:\t\t")
        sleep(0.2)
        print('Подобрали для Вас следующие вакансии:\n')
        match user_input:
            case "1":
                data = db.get_companies_and_vacancies_count()
                get_answers("1", data)
            case "2":
                data = db.get_all_vacancies()
                print(f"Всего вакансий: {len(data)}")
                get_answers("2", data)
            case "4":
                data = db.get_vacancies_with_higher_salary()
                print(f"Всего вакансий: {len(data)}")
                get_answers("4", data)
            case "5":
                input_word = input("Введите слово для поиска:\t\t")
                data = db.get_vacancies_with_keyword(input_word)
                print(f"Всего вакансий: {len(data)}")
                get_answers("5", data)
            case "3":
                data = db.get_avg_salary()
                get_answers("3", data)
        exit_status = input("Подобрать для Вас других вакансий?\n(1 - Да, 2 - Нет)\n")
        if exit_status == '2':
            break
    print("Спасибо за обращение! Хорошего дня!")

# блок выполнения основной функции
if __name__ == '__main__':
    main()