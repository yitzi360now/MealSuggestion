import datetime
import dbConnect

# database connection
cursor = dbConnect.db.cursor()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

email = 'halfonamir1@gmail.com'
query = "select meal_id,meal_date,meal_hour,day_of_week from fitness360db.meals where user_email = '" + email + "'"
cursor.execute(query)
mealTimes = cursor.fetchall()
for meal in mealTimes:
    print(meal)


