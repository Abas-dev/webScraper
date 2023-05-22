from time import sleep
from datetime import datetime
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select


class yerl:

    monthNum = datetime.now().month
    year = str(datetime.now().year)
    month = calendar.month_name[monthNum]
    day = str(datetime.now().day)
    monthYear = month +' '+ year
    monthDayYear = month+day+','+year
    current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
    time=current_time
    
    def run():
        pass