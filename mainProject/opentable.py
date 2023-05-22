from time import sleep
from datetime import datetime
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

class Opentable:

    monthNum = datetime.now().month
    year = str(datetime.now().year)
    month = calendar.month_name[monthNum]
    day = str(datetime.now().day)
    monthYear = month +' '+ year
    monthDayYear = month+day+','+year
    current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
    time=current_time

    def run(self,path,time,month_year=monthYear,day=day,guest=1):
        driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
        driver.get(path)
        driver.maximize_window()
        guestDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[1]/div/select')
        timeDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[3]/div/select')
        dateDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[2]')
        findTableButton = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/button')

        dateDropdown.click()
        sleep(2)

        monthYear = month_year
        found_month_year = False
 
        while not found_month_year:
            getMonthYear = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/div[1]').text
            if monthYear == getMonthYear:
                myDay = str(day)   
                days = driver.find_element(By.XPATH,f"//div[text()='{myDay}']")
                days.click()
                found_month_year = True
                sleep(2)
            else:
                nextBtn = driver.find_element(By.XPATH, '//button[contains(@class, "react-datepicker__navigation--next")]')
                nextBtn.click()
                sleep(2)
              

        gdd = Select(guestDropdown)
        tdd = Select(timeDropdown)

        guest_no = guest - 1
        gdd.select_by_index(guest_no)  #hhh
        
        tdd.select_by_visible_text(time)

        findTableButton.click()

        sleep(3)

        getAvailTime = driver.find_elements(By.XPATH,'//*[@id="panel-home"]/div[1]/div/ul')

        print(getAvailTime)

        for a in getAvailTime:
            print(a.text)

        sleep(5)
