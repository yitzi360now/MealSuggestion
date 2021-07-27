from datetime import datetime
from flask import Flask
import dbConnect

# database connection
cursor = dbConnect.db.cursor()

now = datetime.now()
FMT = '%H:%M:%S'
current_time = now.strftime(FMT)
hour = int(current_time[0:2])
if 6 <= hour < 12:
    partOfDay = 1
elif 12 <= hour < 18:
    partOfDay = 2
else:
    partOfDay = 3

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

# get relevant data about user. General info:
query = "select age,weight,gender,height from fitness360db.users where email='" + email + "'"
cursor.execute(query)
mealInfo = cursor.fetchall()
userAge = mealInfo[0][0]
userWeight = mealInfo[0][1]
userGender = mealInfo[0][2]
userHeight = mealInfo[0][3]
# calorie intake so far today:
query = "select SUM(calories) from fitness360db.meals where user_email='" + email + "' and meal_date = curdate()"
cursor.execute(query)
caloriesYetToday = cursor.fetchall()[0][0]

# calculate calorie target for meal
if userGender:
    calorieTarget = (655 + 1.8 * userHeight + 9.6 * userWeight - 4.7 * userAge) * partOfDay/3 - caloriesYetToday
else:
    calorieTarget = (66 + 5 * userHeight + 13.7 * userWeight - 6.8 * userAge) * partOfDay/3 - caloriesYetToday

print(userAge, userWeight, userGender, userHeight, calorieTarget, caloriesYetToday)

# get relevant meal data about all user's meals in database
query = "select age,weight,meal_id,meal_hour,weekday,gender,calories from fitness360db.meals" \
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
    hour = meal[3] + ':00'
    # print(hour)
    timeDiff1 = datetime.strptime(current_time, FMT) - datetime.strptime(hour, FMT)
    timeDiff2 = datetime.strptime(hour, FMT) - datetime.strptime(current_time, FMT)
    timeDiff = min(timeDiff1.seconds // 60, timeDiff2.seconds // 60)

    # calculate difference between current weekday and day of meal where each day has its own value
    weekdayDiff1 = abs(weekday - meal[4])
    weekdayDiff2 = 7 - weekdayDiff1
    weekdayDiffA = min(weekdayDiff1, weekdayDiff2)
    # print(weekdayDiffA)

    # calculate difference in users data vs user form database
    ageDiff = abs(userAge - meal[0])
    genderDiff = abs(userGender - meal[5])
    weightDiff = abs(userWeight - meal[1])
    personDiff = ageDiff * 10 + genderDiff * 1000 + weightDiff * 20

    # calculate how close meal is to target calorie wise
    calorieDiff = abs(calorieTarget - meal[6])

    # calculate overall difference and save meal id if it is the closest yet
    difference1 = weekdayDiffA * 1000 + timeDiff + personDiff * 2 + calorieDiff * 2
    if difference1 < minDiff1:
        minDiff1 = difference1
        minID1 = meal[2]

    # calculate difference between current weekday and day of meal where each day has binary value of weekend or not
    theDay = int(meal[4])
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
    difference2 = weekdayDiffB * 1000 + timeDiff + personDiff * 2 + calorieDiff * 2
    if difference2 < minDiff2:
        minDiff2 = difference2
        minID2 = meal[4]

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
