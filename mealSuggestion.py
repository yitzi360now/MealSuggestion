from datetime import datetime
from flask import Flask
import dbConnect

# database connection
cursor = dbConnect.db.cursor()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
s1 = '23:48:26'
FMT = '%H:%M:%S'
tdelta = datetime.strptime(current_time, FMT) - datetime.strptime(s1, FMT)
print(tdelta.seconds // 60)
weekday = datetime.today().weekday()
if weekday == 6:
    weekday = 1
else:
    weekday += 2
print("weekday: " + str(weekday))
from flask import Flask

app = Flask(__name__)
email = 'halfonamir1@gmail.com'
query = "select meal_id,meal_date,meal_hour,weekday from fitness360db.meals where user_email = '" + email + "'"
cursor.execute(query)
mealTimes = cursor.fetchall()
minDiff = 99999999999999
minID = 0
for meal in mealTimes:
    print(meal[2])
    hour = meal[2] + ':00'
    print(hour)
    timeDiff1 = datetime.strptime(current_time, FMT) - datetime.strptime(hour, FMT)
    timeDiff2 = datetime.strptime(hour, FMT) - datetime.strptime(current_time, FMT)
    # print(timeDiff.seconds // 60)
    # print(timeDiff2.seconds // 60)
    # print(min(timeDiff.seconds // 60, timeDiff2.seconds // 60))
    timeDiff = min(timeDiff1.seconds // 60, timeDiff2.seconds // 60)
    weekdayDiff1 = abs(weekday - meal[3])
    weekdayDiff2 = 7 - weekdayDiff1
    weekdayDiff = min(weekdayDiff1, weekdayDiff2)
    print(weekdayDiff)
    difference = weekdayDiff * 1000 + timeDiff
    if difference < minDiff:
        minDiff = difference

    print('\n')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)