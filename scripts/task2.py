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

# https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python

connection.close()