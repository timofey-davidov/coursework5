/* Файл-черовик для записей основных запросов в SQL*/
-- Список всех компаний и количество вакасий у каждой компании
SELECT employees.employer_name, COUNT(*) AS vacancies_count
FROM vacancies
JOIN employees USING(employer_id)
GROUP BY employer_name
ORDER BY vacancies_count
LIMIT 10

-- Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
SELECT employees.employer_name, vacancies.vacancy_name, vacancies.salary, vacancies.url
FROM vacancies
JOIN employees USING(employer_id)
ORDER BY vacancies.salary
LIMIT 10

-- Средняя зарплата по вакансиям
SELECT ROUND(AVG(salary), 2) as average_salary
FROM vacancies
ORDER BY average_salary DESC
LIMIT 10

-- Список всех вакансий, у которых зарплата ВЫШЕ СРЕДНЕЙ по всем вакансиям
SELECT(*)
FROM vacancies
WHERE salary > (SELECT AVG(salary) FROM vacancies)
ORDER BY salary DESC
LIMIT 10

-- Список вакансий, в названии которых содержится некоторое слово, например, python
SELECT *
FROM vacancies
WHERE vacancy_name LIKE '%python%'
LIMIT 10