from time import sleep
from datetime import datetime,timedelta
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

class Sevenrooms:

    monthNum = datetime.now().month
    year = str(datetime.now().year)
    month = calendar.month_name[monthNum]
    theDay = datetime.now().day
    day = str(theDay)
    monthYear = month +' '+ year
    monthDayYear = month+day+','+year
    current_time = datetime.now()
    rounded_time = current_time + timedelta(minutes=30 - current_time.minute % 30)
    rounded_time = rounded_time.replace(second=0, microsecond=0).strftime("%I:%M %p").lstrip("0").lower()


    def run(self,path,time=rounded_time,day=day,guest=1,month_year=monthYear):
        driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

        driver.get(path)

        driver.maximize_window()

        opentDateField = driver.find_element(By.XPATH,'//*[@id="sr-search-initial-comp"]/div').click()

        sleep(2)

        for i in range(12):
            monthYear = month_year
            getMonthYear = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/div/span[1]').text
            if monthYear == getMonthYear:
                selectedDay = str(day)
                getDay = driver.find_element(By.XPATH,f"//td[text()='{selectedDay}']")
                getDay.click()
                break
            else:
                arrowbtn = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/button[2]').click()
                print('arrow clicked')
        sleep(2)

        driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[2]/div/div').click()
        numberOfGuest = str(guest)
        driver.find_element(By.XPATH,f"//button[text()='{numberOfGuest}']").click()

        sleep(2)

        driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[3]/div/div').click()
        selectedTime = time
        driver.find_element(By.XPATH,f"//button[text()='{selectedTime}']").click()

        sleep(2)    

        driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[4]/div/button').click()

        sleep(8)

        getResult = driver.find_elements(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[3]')

        if len(getResult) > 0:
            for a in getResult:
                print('day for resevation',day)
                print('time for reservations',a.text)
                break
        else:
            self.theDay = self.theDay + 1 
            day = str(self.theDay)
            self.run(day=day,path=path,time=time)
            driver.refresh()     