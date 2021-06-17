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
minDiff1 = 99999999999999
minID1 = 0
minDiff2 = 99999999999999
minID2 = 0
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
    weekdayDiffA = min(weekdayDiff1, weekdayDiff2)
    print(weekdayDiffA)
    difference1 = weekdayDiffA * 1000 + timeDiff
    if difference1 < minDiff1:
        minDiff1 = difference1
        minID1 = meal[0]
    theDay = int(meal[3])
    if theDay < 6:
        theDay = 0
    else:
        theDay = 1
    if weekday < 6:
        weekday = 0
    else:
        weekday = 1
    weekdayDiffB = abs(weekday - theDay)
    print(weekdayDiffB)
    difference2 = weekdayDiffB * 1000 + timeDiff
    if difference2 < minDiff2:
        minDiff2 = difference2
        minID2 = meal[0]
# print results based on first algorithm
query = "select * from fitness360db.meals where meal_id =" + str(minID1)
cursor.execute(query)
bestMeal1 = cursor.fetchall()
print(bestMeal1)
print(minDiff1)
print('----------------------------')
# print results based on second algorithm
query = "select * from fitness360db.meals where meal_id =" + str(minID2)
cursor.execute(query)
bestMeal2 = cursor.fetchall()
print(bestMeal2)
print(minDiff2)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)
