import psycopg2

from config import config
from utils import get_companies, get_vacancies, create_db, save_data_to_db
from db_manager import DBManager


def main():
    companies_data = get_companies()
    vacancies_data = get_vacancies(companies_data)
    params = config()

    create_db('vacancies_hh', params)

    conn = psycopg2.connect(dbname='vacancies_hh', **params)
    save_data_to_db(companies_data, vacancies_data, 'vacancies_hh', params)
    conn.close()

    conn = psycopg2.connect(dbname='vacancies_hh', **params)
    db_manager = DBManager(conn)

    print('Кнопки управления:\n'
          '1: - Показать список всех компаний и количество вакансий у каждой компании\n'
          '2: - Показать список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n'
          '3: - Показать среднюю зарплату по вакансиям\n'
          '4: - Показать список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
          '5: - Показать cписок всех вакансий, в названии которых содержатся переданные в метод слова\n'
          'stop: - Закончить работу'
          )
    user_input = input()
    if user_input == '1':
        companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
        print("Компании и количество доступных вакансий:")
        for company_name, vacancy_counter in companies_and_vacancies_count:
            print(f"{company_name}: {vacancy_counter}")
    elif user_input == '2':
        all_vacancies = db_manager.get_all_vacancies()
        print("Все вакансии:")
        for vacancy in all_vacancies:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max}, "
                  f"Ссылка на вакансию: {vacancy_url}")
    elif user_input == '3':
        avg_salary = db_manager.get_avg_salary()
        print(f"Средняя зарплата по всем вакансиям: {avg_salary}")
    elif user_input == '4':
        higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
        print("Вакансии с зарплатой выше средней:")
        for vacancy in higher_salary_vacancies:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max},"
                  f"Ссылка на вакансию: {vacancy_url}")
    elif user_input == '5':
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
        print(f"Все вакансии с ключевым словом '{keyword}':")
        for vacancy in vacancies_with_keyword:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max},"
                  f"Ссылка на вакансию: {vacancy_url}")
    else:
        print("Некорректный ввод")

    db_manager.__del__()
    conn.close()


if __name__ == '__main__':
    main()
