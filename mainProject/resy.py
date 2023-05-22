from time import sleep
from datetime import datetime
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

class Resy:

    monthNum = datetime.now().month
    year = str(datetime.now().year)
    month = calendar.month_name[monthNum]
    day = str(datetime.now().day)
    monthYear = month +' '+ year
    monthDayYear = month+day+','+year
    current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
    time=current_time

    def run(self,path,guest=1,month_year=monthYear,month_day_year=monthDayYear):
        
        driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

        driver.get(path)

        driver.maximize_window()

        sleep(4)
        
        guest_no = guest - 1
        guestDropdown = driver.find_element(By.ID,'party_size')
        gdd = Select(guestDropdown)
        gdd.select_by_index(guest_no)

        sleep(2)

        driver.find_element(By.ID,'DropdownGroup__selector--date--selection').click()

        sleep(2)

        for c in range(12):
            sleep(2)
            getMonthYear = driver.find_element(By.XPATH,"//h2[@class='CalendarMonth__Title']").text
            
            print(getMonthYear)
            monthYear = month_year
            if monthYear == getMonthYear:    
                days = driver.find_elements(By.XPATH,f'//button[@aria-label="{month_day_year}"]')
                
                for i in days:
                    if i.get_attribute('aria-label')==(month_day_year):
                        i.click()
                        sleep(5)
                        break
                break    
            else:
                nextBtn = driver.find_element(By.XPATH,'//button[contains(@class, "ResyCalendar__nav_right Button Button--primary Button--circle")]')
                nextBtn.click()
                print('btn clicked')
                sleep(2)

        sleep(2)

        reseveationsTime = driver.find_elements(By.XPATH,'//*[@id="page-content"]/venue-page/div/div[1]/div[1]/div[2]/div[3]')

        for i in reseveationsTime:
            print(i.text)