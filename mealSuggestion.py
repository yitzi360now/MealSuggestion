from datetime import datetime
import dbConnect

# database connection
cursor = dbConnect.db.cursor()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
s1 = '23:48:26'
FMT = '%H:%M:%S'
tdelta = datetime.strptime(current_time, FMT) - datetime.strptime(s1, FMT)
print(tdelta.seconds // 60)
print("weekday: " + str(datetime.today().weekday()))

email = 'halfonamir1@gmail.com'
query = "select meal_id,meal_date,meal_hour,day_of_week from fitness360db.meals where user_email = '" + email + "'"
cursor.execute(query)
mealTimes = cursor.fetchall()
minDistance = 99999999999999
minID = 0
for meal in mealTimes:
    print(meal[2])
    hour = meal[2] + ':00'
    print(hour)
    difference = datetime.strptime(current_time, FMT) - datetime.strptime(hour, FMT)
    difference2 = datetime.strptime(hour, FMT) - datetime.strptime(current_time, FMT)
    # print(difference.seconds // 60)
    # print(difference2.seconds // 60)
    # print(min(difference.seconds // 60, difference2.seconds // 60))
    timeDiff = min(difference.seconds // 60, difference2.seconds // 60)
    print('\n')
