import psycopg2
from psycopg2 import errors
from utils.config import config

class DBManager:
    def __init__(self, db_name: str, db_params: dict):
        self.db_name = db_name
        self.db_params = db_params

    def create_database(self):
        """Метод для создания базы данных"""
        conn = psycopg2.connect(dbname="postgres", **self.db_params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
            cur.execute(f'CREATE DATABASE {self.db_name}')

        except errors.ObjectInUse:
            cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid)"
                        f"FROM pg_stst_activity"
                        f"WHERE pg_stat_activity.datname = '{self.db_name}'"
                        f"AND pid <> pg_backend_pid();")

        finally:
            cur.close()
            conn.close()

        conn = psycopg2.connect(dbname=self.db_name, **self.db_params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"CREATE TABLE IF NOT EXISTS employees"
                        f"("
                        f"employer_id INT PRIMARY KEY,"
                        f"employer_name VARCHAR(255) UNIQUE NOT NULL"
                        f")")
            cur.execute(f"CREATE TABLE IF NOT EXISTS vacancies"
                        f"("
                        f"vacancy_id INT PRIMARY KEY,"
                        f"vacancy_name VARCHAR(255) NOT NULL,"
                        f"vacancy_description TEXT,"
                        f"employer_id INT REFERENCES employees(employer_id),"
                        f"salary INT,"
                        f"date_piblished DATE,"
                        f"url TEXT"
                        f")")
        finally:
            cur.close()
            conn.close()

    def add_data(self, table_name: str, data: dict):
        """Метод добавления данных в базу данных"""
        conn = psycopg2.connect(dbname=self.db_name, **self.db_params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            match table_name:
                case "employees":
                    cur.execute('INSERT INTO employees (employer_id, employer_name) VALUES (%s, %s)', (data['id'], data['title']))
                case "vacancies":
                    cur.execute("INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_description, salary, date_piblished, url, employer_id)"
                                "VALUES (%s, %s, %s, %s, %s, %s, %s)", (data['vacancy_id'], data['vacancy_name'], data['vacancy_description'], data['salary'], data['date_published'], data['url'], data["employer_id"]))
        finally:
            cur.close()
            conn.close()


    def get_query_result(self, query) -> list:
        """Метод для возврата результата запроса"""
        conn = psycopg2.connect(dbname=self.db_name, **self.db_params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(query)
            query_result = cur.fetchall()
        finally:
            cur.close()
            conn.close()
        return query_result

    def get_companies_and_vacancies_count(self):
        """
        Функция для получения списка всех компаний и количества вакансий у каждой компании
        """
        query = f"SELECT employees.employer_name, COUNT(*) AS vacancies_count FROM vacancies JOIN employees USING(employer_id) GROUP BY employer_name ORDER BY vacancies_count"
        result = self.get_query_result(query)
        return result

    def get_all_vacancies(self):
        """
        Функция для получения всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию
        """
        query = f"SELECT employees.employer_name, vacancies.vacancy_name, vacancies.salary, vacancies.url FROM vacancies JOIN employees USING(employer_id) ORDER BY vacancies.salary LIMIT 10"
        result = self.get_query_result(query)
        return result

    def get_avg_salary(self):
        """
        Функция для получения средней заработной платы по вакансиям
        """
        query = f"SELECT ROUND(AVG(salary), 2) as average_salary FROM vacancies ORDER BY average_salary DESC LIMIT 10"
        result = self.get_query_result(query)
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Функция для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        query = f"SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies) ORDER BY salary DESC LIMIT 10"
        result = self.get_query_result(query)
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Функция для получения всех вакансий, в названии еоторых содержится переданные в метод слова
        """
        query = f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{keyword}%' LIMIT 10"
        result = self.get_query_result(query)
        return result

if __name__ == '__main__':
    db =DBManager("hh", config('../utils/database.ini'))
    query1 = f"SELECT ROUND(AVG(salary), 2) as average_salary FROM vacancies ORDER BY average_salary DESC"
    res = db.get_query_result(query1)
    print(res)