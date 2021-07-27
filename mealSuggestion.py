from datetime import datetime
from flask import Flask
import dbConnect

# database connection
cursor = dbConnect.db.cursor()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
FMT = '%H:%M:%S'
weekday = datetime.today().weekday()
if weekday == 6:
    weekday = 1
else:
    weekday += 2

# get username from client
app = Flask(__name__)

# @app.route('/data')
# def data():
#     # here we want to get the value of user (i.e. ?user=some-value)
# user = request.args.get('user')
email = 'yitzi9@hotmail.com'

# get relevant data about user
query = "select age,weight,gender from fitness360db.users where email='" + email + "'"
cursor.execute(query)
mealInfo = cursor.fetchall()
userAge = mealInfo[0][0]
userWeight = mealInfo[0][1]
userGender = mealInfo[0][2]
print(userAge, userWeight, userGender)

# get relevant meal data about all user's meals in database
query = "select email,age,weight,meal_id,meal_date,meal_hour,weekday,gender from fitness360db.meals" \
        " join fitness360db.users ON (fitness360db.meals.user_email=fitness360db.users.email)"
cursor.execute(query)
mealTimes = cursor.fetchall()

#  algorithm finds best fitting meal with minimal 'distance' based on hour of day and doy of week
minDiff1 = 99999999999999
minID1 = 0
minDiff2 = 99999999999999
minID2 = 0
for meal in mealTimes:
    # calculate difference between current time and time of meal
    hour = meal[5] + ':00'
    # print(hour)
    timeDiff1 = datetime.strptime(current_time, FMT) - datetime.strptime(hour, FMT)
    timeDiff2 = datetime.strptime(hour, FMT) - datetime.strptime(current_time, FMT)
    timeDiff = min(timeDiff1.seconds // 60, timeDiff2.seconds // 60)

    # calculate difference between current weekday and day of meal where each day has its own value
    weekdayDiff1 = abs(weekday - meal[6])
    weekdayDiff2 = 7 - weekdayDiff1
    weekdayDiffA = min(weekdayDiff1, weekdayDiff2)
    # print(weekdayDiffA)

    # calculate difference in users data vs user form database
    ageDiff = abs(userAge - meal[1])
    genderDiff = abs(userGender - meal[7])
    weightDiff = abs(userWeight - meal[2])
    personDiff = ageDiff * 10 + genderDiff * 1000 + weightDiff * 20

    # calculate overall difference and save meal id if it is the closest yet
    difference1 = weekdayDiffA * 1000 + timeDiff
    difference1 += personDiff
    if difference1 < minDiff1:
        minDiff1 = difference1
        minID1 = meal[3]

    # calculate difference between current weekday and day of meal where each day has binary value of weekend or not
    theDay = int(meal[6])
    if theDay < 6:
        theDay = 0
    else:
        theDay = 1
    if weekday < 6:
        weekday = 0
    else:
        weekday = 1
    weekdayDiffB = abs(weekday - theDay)
    # print(weekdayDiffB)

    # calculate overall difference and save meal id if it is the closest yet
    difference2 = weekdayDiffB * 1000 + timeDiff
    difference2 += personDiff
    if difference2 < minDiff2:
        minDiff2 = difference2
        minID2 = meal[3]

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

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


# if __name__ == '__main__':
#     app.run(debug=True)
