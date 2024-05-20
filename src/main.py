import psycopg2
from src.db_manager import DBManager
from src.utils import save_data_to_db, get_vacancies, get_companies, create_db
from src.config import config


def main():
    companies_data = get_companies()
    vacancies_data = get_vacancies(companies_data)
    params = config()

    create_db('vacancies', params)

    conn = psycopg2.connect(dbname='vacancies', **params)
    save_data_to_db(companies_data, vacancies_data, 'vacancies', params)
    conn.close()

    conn = psycopg2.connect('vacancies', **params)
    db_manager = DBManager(conn)

    while True:
        print('Кнопки управления:\n'
              '1: - Показать список всех компаний и количество вакансий у каждой компании\n'
              '2: - Показать список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n'
              '3: - Показать среднюю зарплату по вакансиям\n'
              '4: - Показать список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
              '5: - Показать cписок всех вакансий, в названии которых содержатся переданные в метод слова\n'
              'stop: - Закончить работу'
              )
        answer = input()
        if answer == "стоп" or answer == "stop":
            break
        answer = int(answer)
        if answer == 1:
            db_manager.get_companies_and_vacancies_count()
        elif answer == 2:
            db_manager.get_all_vacancies()
        elif answer == 3:
            db_manager.get_avg_salary()
        elif answer == 4:
            db_manager.get_vacancies_with_higher_salary()
        elif answer == 5:
            print('Введите ключевое слово: ')
            keyword = input()
            db_manager.get_vacancies_with_keyword(keyword)
        else:
            print('Введите цифру от 1 до 5')

if __name__ == '__main__':
    main()



