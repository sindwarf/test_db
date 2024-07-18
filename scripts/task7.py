from mysql.connector import connect, Error
from env import secrets
from pymongo import MongoClient


# MONGODB_URI = "mongodb+srv://jonathansindorf:sLCFinPHKGrN2OX4@airbnbcluster.onda5us.mongodb.net/?retryWrites=true&w=majority&appName=AirBNBCluster"



def get_file_as_string(filename):
    fileString = ''
    with open(filename, 'r') as f:
        fileString = f.read()
    
    return fileString

def createMongoDB():
    # connect to local mongo client
    client = MongoClient('127.0.0.1', 27017)

    db = client['employee_appreciation']

    # try:
    #     db.drop_collection('bonuses')
    # except:
    #     pass

    try:
        db.create_collection('bonuses')
    except:
        print("collection already exists")
        collection = db['bonuses']
        return collection
    
    collection = db['bonuses']
    collection.insert_many([
    { 'yearsOfService': 1, 'bonusAmount': 50 },
    { 'yearsOfService': 5, 'bonusAmount': 500 },
    { 'yearsOfService': 10, 'bonusAmount': 1000 },
    { 'yearsOfService': 15, 'bonusAmount': 1500 },
    { 'yearsOfService': 20, 'bonusAmount': 3000 },
    { 'yearsOfService': 25, 'bonusAmount': 4000 },
    { 'yearsOfService': 30, 'bonusAmount': 5000 }
    ])



def main():
    db_user=secrets.get('DATABASE_USER')
    db_host=secrets.get('DATABASE_HOST')

    try:
        connection = connect(user=db_user, host=db_host, database="employees")
    except Error as e:
        print(e)


    collection = createMongoDB()

    yearsOfService = [10, 20, 25]
    empBonuses = []
    cursor = connection.cursor()
    mongoCursor = collection.find({})
    for years in yearsOfService:
        cursor.execute(f'''
                        SELECT emp_no, first_name, last_name
                        FROM employees
                        WHERE TIMESTAMPDIFF(year, hire_date, now()) = {years};
                    ''')
        mongoCursor = collection.find_one({'yearsOfService': years})
        empBonuses.append((cursor.fetchall(), mongoCursor['bonusAmount']))

    reportString = '#Employee Bonuses\n'

    for i, employees in enumerate(empBonuses):
        reportString += f"For {yearsOfService[i]} years:\n"
        for j, employee in enumerate(employees[0]):
            reportString += f'{j+1}. {employee[1]} {employee[2]} recieves ${employees[1]}.\n'

    with open("bonus_report.md", 'w') as f:
        f.write(reportString)

if __name__ == "__main__":
    main()


'''
One last task that this employer would like you to assist with is a creating a list, to be delivered to the administrative assistant, of employee appreciation gifts depending on number of years of service. Below is the code to construct the small Mongo database that stores information about years of service and the gift that is delivered depending on the number of years of service. Currently, the employer wishes to recognize those employees with 10 or 20 years of service. Please create a report, in any format you wish, that utilizes both the MySQL database you have been using with results pulled programmatically from the MongoDB listing employees and the gift they will receive based on years of service.

They have their script for this database Download script for this databasestored as a RTF file. Use/modify their code as needed to appropriately construct the employee appreciation MongoDB database.


'''
'''
1. Create mongo database if it doesn't exist
2. Pull all employees who have 10 - 19.9 years of service
3. Put them in a list with the correct bonus, pulled from mongo
4. Pull all employees who have 20+ years of service
5. Put them in a list with the correct bonus, pulled from mongo
6. Write a report with a list of employees and their correct bonuses
'''