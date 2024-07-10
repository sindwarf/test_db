from mysql.connector import connect, Error
from env import secrets

db_user=secrets.get('DATABASE_USER')
db_host=secrets.get('DATABASE_HOST')

try:
    connection =  connect(user=db_user, host=db_host, database="employees")
except Error as e:
    print(e)

mycursor = connection.cursor()

mycursor.execute('select * from departments')

result = mycursor.fetchall()

print(result)

connection.close()


'''
    As per the company's decision, the CEO has initiated a workforce restructuring plan, resulting in the termination of half the employees. To ensure fairness, the terminated employees have been randomly selected, and their employee numbers compiled in a CSV file. employees_cuts.csv Download employees_cuts.csv

    Your task is to develop a solution that reads the employee numbers from the CSV file and updates their employment status in the database accordingly. It is crucial to maintain data integrity and avoid permanently deleting employee records.

    Instructions:

    Design an Update Strategy:
    Create a strategy to update the employment status of the employees listed in the CSV file.
    Assign a specific status code, such as 'T' (terminated), to indicate the updated employment status.
    Consider adding a new field, such as 'termination_date,' to record the date of termination for future reference.
    Update the Database:
    Develop a program or script to read the employee numbers from the CSV file.
    Connect to the database using your chosen programming language or tool.
    Implement the update strategy to modify the employment status of the selected employees in the database.
    Update the 'employment_status' field to reflect the termination using the assigned status code ('T').
    Preserve Data Integrity:
    Ensure that the updated employment status accurately reflects the termination of the selected employees.
    Verify that the data in the database remains intact, with no permanent deletion of employee records.
    Consider using transactions or backup mechanisms to safeguard against accidental data loss.
'''

'''
    
'''