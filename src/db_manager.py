class DBManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cursor.execute('''
            SELECT c.company_name, COUNT(*) AS vacancy_count
            FROM companies c
            JOIN vacancies v USING(company_id)
            GROUP BY c.company_name;
        ''')
        for i in self.cursor.fetchall():
            print(i)

    def get_all_vacancies(self):
        self.cursor.execute('''
            SELECT c.company_name, v.vacancy_name, v.salary_min, v.salary_max, v.vacancy_url
            FROM companies c
            JOIN vacancies v USING(company_id);  
        ''')
        for i in self.cursor.fetchall():
            print(i)

    def get_avg_salary(self):
        self.cursor.execute('''
            SELECT ROUND(AVG((salary_min + salary_max) / 2)) AS average_salary 
            FROM vacancies;
        ''')
        return self.cursor.fetchone[0]

    def get_vacancies_with_higher_salary(self):
        self.cursor.execute('''
            SELECT * from vacancies
            WHERE (salary_min + salary_max) / 2 > 
            (SELECT AVG(salary_min + salary_max) / 2) FROM vacancies; 
        ''')
        for i in self.cursor.fetchall():
            print(i)

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute('''
            SELECT * FROM vacancies
            WHERE vacancy_name '%%' || %s || '%%';
        ''', (keyword,))

        list = self.cursor.fetchall()
        if len(list) == 0:
            print('По такому ключевому слову вакансии не найдены')
            print()
        else:
            for i in list:
                print(i)


    def __del__(self):
        self.cursor.close()
