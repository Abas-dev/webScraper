from datetime import datetime
import calendar
monthNum = datetime.now().month
year = str(datetime.now().year)
month = calendar.month_name[monthNum]
day = str(datetime.now().day)
monthYear =month,year
monthDayYear=month,day+',',year
current_time = datetime.now().strftime("%I:%M %p")
time=current_time

day = '1'

day = int(day) +1

day = str(day)

print (type(day))
