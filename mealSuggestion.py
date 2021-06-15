import dbConnect

cursor = dbConnect.db.cursor()
query = "select * from fitness360db.groups"
cursor.execute(query)
tables = cursor.fetchall()
for table in tables:
    print(table)

