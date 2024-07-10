from mysql.connector import connect, Error
from env import secrets

def get_file_as_string(filename):
    fileString = ''
    with open(filename, 'r') as f:
        fileString = f.read()
    
    return fileString


def update_company_emails():
    global connection
    cursor = connection.cursor()
    cursor.execute('SELECT emp_no FROM employees WHERE company_email IS NULL')
    totalEmployees = cursor.fetchall()
    # print('total:', totalEmployees)
    for emp_no in totalEmployees:
        # print(emp_no[0])
        try:
            cursor.execute(
                f'UPDATE employees\
                SET company_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, "@company.net")\
                WHERE emp_no = {emp_no[0]}'
            )
        except Exception as e:
            maxAttempts = 99
            curIteration = 1
            while(curIteration < maxAttempts):
                try:
                    cursor.execute(
                        f'UPDATE employees\
                        SET company_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, {curIteration}, "@company.net")
                        WHERE emp_no = {emp_no[0]}'
                    )
                    # cursor.execute(f'select * from employees where emp_no = {emp_no[0]}')
                    # print(cursor.fetchone())
                    break
                except:
                    curIteration += 1
            else:
                raise Exception("Exceeded max attempts to insert employee, something may be wrong or you need to increase your max attempts")
            # print(f'{e}')
    print("Done updating company emails")
    connection.commit() 

def update_personal_emails():
    global connection
    cursor = connection.cursor()
    cursor.execute(
        'SELECT emp_no\
        FROM employees\
        WHERE emp_no in (\
            SELECT emp_no\
            FROM titles\
            WHERE title REGEXP "senior") AND personal_email IS NULL'
        )
    seniorEmployees = cursor.fetchall()
    # print(seniorEmployees)
    for emp_no in seniorEmployees:
        try:
            cursor.execute(
                f'UPDATE employees \
                SET personal_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, "@personal.net")\
                WHERE emp_no = {emp_no[0]}'
                )
        except Exception as e:
            maxAttempts = 99
            curIteration = 1
            while(curIteration < maxAttempts):
                try:
                    cursor.execute(
                        f'UPDATE employees\
                        SET personal_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, {curIteration}, "@personal.net")\
                        WHERE emp_no = {emp_no[0]}')
                    # cursor.execute(f'select * from employees where emp_no = {emp_no[0]}')
                    # print(cursor.fetchone())
                    break
                except:
                    curIteration += 1
            else:
                raise Exception("Exceeded max attempts to insert employee, something may be wrong or you need to increase your max attempts")
            # print(f'\n\n{e}')
    print("Done updating personal emails")
    connection.commit()

def main():
    global connection
    db_user=secrets.get('DATABASE_USER')
    db_host=secrets.get('DATABASE_HOST')

    try:
        connection =  connect(user=db_user, host=db_host, database="employees")
    except Error as e:
        print(e)

    cursor = connection.cursor()
    # Create new columns
    try:
        cursor.execute('ALTER TABLE employees\
        ADD COLUMN company_email varchar(64) UNIQUE,\
        ADD COLUMN personal_email varchar(64) UNIQUE,\
        ADD COLUMN phone varchar(64)')
        connection.commit()
    except:
        print("Columns already created.")
        connection.rollback()
    # Create stored procedure for updating company_phones
    try:
        cursor.execute(get_file_as_string('task3.sql'))
        connection.commit()
    except:
        print("File could not execute")
        connection.rollback()
    cursor.execute('call update_company_phone()')
    connection.commit()
    
    update_company_emails()
    update_personal_emails()


    connection.close()

if __name__ == "__main__":
    main()

