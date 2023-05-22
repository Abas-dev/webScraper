from datetime import datetime, timedelta
import calendar
monthNum = datetime.now().month
year = str(datetime.now().year)
month = calendar.month_name[monthNum]
day = str(datetime.now().day)
monthYear =month,year
monthDayYear=month,day+',',year
current_time = datetime.now().strftime("%I:%M %p")
time=current_time

# day = '1'

# day = int(day) +1

# day = str(day)

# print (type(day))

tm = datetime.now().strftime("%I").lstrip("0")
print(tm)

current_time = datetime.now()
rounded_time = current_time + timedelta(minutes=30 - current_time.minute % 30)
rounded_time = rounded_time.replace(second=0, microsecond=0).strftime("%I:%M %p").lstrip("0")

print(rounded_time)