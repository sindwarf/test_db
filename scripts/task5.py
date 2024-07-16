from mysql.connector import connect, Error
from env import secrets

def get_file_as_string(filename):
    fileString = ''
    with open(filename, 'r') as f:
        fileString = f.read()
    
    return fileString

def main():
    db_user=secrets.get('DATABASE_USER')
    db_host=secrets.get('DATABASE_HOST')

    try:
        connection = connect(user=db_user, host=db_host, database="employees")
    except Error as e:
        print(e)

    cursor = connection.cursor()
    
    # Verify job titles match the criteria we are using to update
    cursor.execute('SELECT COUNT(emp_no) FROM employees WHERE employment_status IS NULL')
    if cursor.fetchone()[0] != 0:
        raise Exception("Error: No employees should have an employement status of NULL")
    
    jobTitles = ["Assistant Engineer", "Engineer","Manager", "Senior Engineer", "Staff", "Technique Leader", "Senior Staff"]

    cursor.execute('SELECT DISTINCT title from titles')

    existingTitles = cursor.fetchall()
    if len(jobTitles) != len(existingTitles):
        raise Exception("Error: amount of known titles does not match actual amount.")
    
    for title in existingTitles:
        if title[0] not in jobTitles:
            raise Exception("Error: Existing and known job titles do not match")

    # Collect salary data to verify the calculation is done correctly
    verificationSalaries = []
    # If salary/to_date is 9999-01-01 we know that the employee is currently employed, no need to check employees table
    for title in jobTitles:
        cursor.execute(f'''
            SELECT
                salary
            FROM
                salaries
            WHERE
                to_date = '9999-01-01'
            AND emp_no IN (
                SELECT emp_no
                FROM titles
                WHERE title = '{title}'
                AND to_date = '9999-01-01')
            ORDER BY salary
            LIMIT 3''')
        verificationSalaries.append((title, cursor.fetchall()))

    raiseAmount = [("Assistant Engineer", .05),
                    ("Engineer", .075),
                    ("Manager", .1),
                    ("Senior Engineer", .07), 
                    ("Staff", .05), 
                    ("Technique Leader", .08),
                    ("Senior Staff", .065)]

    for item in raiseAmount:
        updateQuery = f'''
            UPDATE
                salaries
            SET 
                salary = (salary + (salary * {item[1]}))
            WHERE
                to_date = '9999-01-01'
            AND
                emp_no IN (
                SELECT emp_no
                FROM titles
                WHERE title = '{item[0]}'
                AND to_date = '9999-01-01')
        '''
        cursor.execute(updateQuery)
        print("Updated: ", item[0])

    postUpdateSalaries = []
    for title in jobTitles:
        cursor.execute(f'''
            SELECT
                salary, emp_no
            FROM
                salaries
            WHERE
                to_date = '9999-01-01'
            AND emp_no IN (
                SELECT emp_no
                FROM titles
                WHERE title = '{title}'
                AND to_date = '9999-01-01')
            ORDER BY salary
            LIMIT 3''')
        postUpdateSalaries.append((title, cursor.fetchall()))
    
    for i, set in enumerate(verificationSalaries):
        for j, value in enumerate(verificationSalaries[i][1]):
            preUpdateSalary = verificationSalaries[i][1][j][0]
            postUpdateSalary = postUpdateSalaries[i][1][j][0] 
            expectedSalary = round(preUpdateSalary + (preUpdateSalary) * raiseAmount[i][1])

            if(expectedSalary != postUpdateSalary):
                connection.rollback()
                raise Exception(f'''
                Values were not calculated correctly
                Original: {preUpdateSalary}
                New: {postUpdateSalary}
                Expected: {expectedSalary}
                ''')
    
    print("Verified Salaries updated correctly")

    connection.commit()

    connection.close()


if __name__ == "__main__":
    main()


'''
0. Check there are no employees with a status of null
0.5 Verify there are no extra job titles other than the ones mentioned
1. Select 3 of each title's salaries to use to verify later
    a. Assistant Engineer
    b. Engineer
    c. Manager
    d. Senior Engineer
    e. Staff
    f. Technique Leader
    g. Senior Staff
2. Run query to update salaries of current employees based upon their title
3. Select the same 3 of each title's salaries
4. Compare with the previous salaries and verify they were all increased by the correct amount

'''