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
    # Create Columns
    try:
        cursor.execute('ALTER TABLE employees\
        ADD COLUMN employment_status ENUM("T", "E"),\
        ADD COLUMN termination_date date')
        connection.commit()
    except:
        print("Columns already created.")
        connection.rollback()
 
    # Import terminated employees as temporary table
    cursor.execute('CREATE TEMPORARY TABLE terminate_employees\
    (\
        emp_no int\
    )')

    cursor.execute("LOAD DATA LOCAL INFILE '../employees_cuts.csv'\
    INTO TABLE\
        terminate_employees\
    FIELDS TERMINATED BY ','\
    LINES TERMINATED BY '\n'\
    IGNORE 1 LINES")

    # Verify count to be compared later
    cursor.execute('SELECT COUNT(*) FROM employees')
    original_entries = cursor.fetchone()[0]

    # Terminated employees are marked by T and employed employees are marked by E
    cursor.execute('\
    UPDATE \
        employees\
    SET\
	    employment_status = "T", termination_date = CURDATE()\
    WHERE\
        emp_no IN (\
            SELECT emp_no FROM terminate_employees\
        )')
    
    cursor.execute('\
    UPDATE \
        employees\
    SET\
	    employment_status = "E"\
    WHERE\
        emp_no NOT IN (\
            SELECT emp_no FROM terminate_employees\
        )')

    cursor.execute('SELECT COUNT(*) FROM employees')

    if (original_entries == cursor.fetchone()[0]):
        print("Verified all rows preserved")
        connection.commit()
    else:
        print("Something went wrong updating employee status: Row(s) were deleted")
        connection.rollback()
        exit(1)
    
    # Create procedure that updates the to_date fields of titles, salaries, dept_manager, and dept_emp tables for terminated employees with dates that have not been updated yet
    # Might be appropriate to call this procedure in a trigger after insert
    try:
        cursor.execute(get_file_as_string('task4.sql'))
    except:
        print("Stored procedure already exists")

    cursor.execute('call update_terminated_employee_dates()')
    connection.commit()

    connection.close()


if __name__ == "__main__":
    main()


'''
1. Create termination status and termination date columns
2. Collect all numbers from CSV
    a. Can do this from python and store in an array
    b. Can try and import this as a temporary table in sql
3. Check current count of employees in employees table
4. Update the fields for each terminated employee
5. Compare current count to previous count
6. Update the To Date for all related fields that are null
    a. dept_emp
    b. dept_manager
    c. salaries
    d. title
'''