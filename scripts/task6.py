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

    allTitles = []

    query = '''
        SELECT DISTINCT title from titles;
    '''
    cursor.execute(query)
    for row in cursor.fetchall():
        allTitles += row
    
    # Using a to_date of 9999-01-01 ensures that we are only looking at currently employed salaries
    query = '''
        SELECT t.title, AVG(s.salary)
        FROM salaries s JOIN titles t on s.emp_no = t.emp_no
        WHERE s.to_date = '9999-01-01'
        GROUP BY title
        ORDER BY title
    '''
    cursor.execute(query)
    averageSalaries = cursor.fetchall()

    query = '''
        SELECT title, COUNT(title)
        FROM titles
        WHERE to_date = '9999-01-01'
        GROUP BY title 
        ORDER BY title
    '''
    cursor.execute(query)
    titleCount = cursor.fetchall()

    forecastedCost = []

    for i, salary in enumerate(averageSalaries):
        # print(titleCount[i])
        forecastedCost.append((averageSalaries[i][0], round(averageSalaries[i][1] * titleCount[i][1], 2)))

    
    print(forecastedCost)

    # connection.commit()

    connection.close()


if __name__ == "__main__":
    main()


'''
Retrieve Employee Salaries and Job Titles:
Query the database to retrieve the salaries and job titles of all employees.
Ensure that terminated employees are excluded from the salary projection report.
Group Salaries by Job Title:
Group the employee salaries based on their job titles.
Calculate the total salary amount for each job title.
Calculate the Projected Expenses:
Multiply the total salary amount for each job title by the number of employees with that job title.
Exclude the terminated employees from the calculation.
Generate the Salary Projection Report:
Format the report in a clear and organized manner.
Include a table or list that displays each job title along with the projected expenses for that title.
Arrange the job titles in ascending or descending order based on the projected expenses.
Add a title or heading to the report that clearly indicates its purpose.
Mention any assumptions or considerations made during the projection process.
Include a summary or conclusion section that highlights the total projected expenses for all job titles.
'''
'''
1. Select the average of salaries of current employees and group by job title and save data.
2. Select the count of current employees for each job title
3. Multiply the average salary by the count for each job title
4. 

'''