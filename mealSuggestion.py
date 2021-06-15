import mysql.connector as mysql

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="matthews34",
    database="fitness360db"
)

cursor = db.cursor()
query = "select * from fitness360db.groups"
cursor.execute(query)
tables = cursor.fetchall()
for table in tables:
    print(table)

# test2