from time import sleep
from datetime import datetime
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select


class Yelp:

    monthNum = datetime.now().month
    year = str(datetime.now().year)
    month = calendar.month_name[monthNum]
    day = str(datetime.now().day)
    monthYear = month +' '+ year
    monthDayYear = month+day+','+year
    current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
    time=current_time
    
    def run(self,path,time,day=day,guest=1,month_year=monthYear):
        driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
        driver.get(path)

        sleep(2)
        driver.find_element(By.XPATH,'//div[contains(@class, "DayPickerInput")]').click()

        foundMonthYear = False
        sleep(2)

        while not foundMonthYear:
            sleep(2)
            monthYear = month_year
            getMonthYear = driver.find_element(By.XPATH,'//*[@id="react-mount-search-widget"]/div/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div').text

            if monthYear == getMonthYear: 
                theDay = day
                driver.find_element(By.XPATH,f'//p[text()="{theDay}"]').click()
                foundMonthYear = True
                sleep(2)
            else:
                nextBtn = driver.find_element(By.XPATH, '//span[contains(@class, "DayPicker-NavButton DayPicker-NavButton--next")]')
                nextBtn.click()
                sleep(2)

        openTime = driver.find_element(By.XPATH,'(//select[contains(@class, "yselect-with-icon search-widget_input--select")])[1]')
        otd = Select(openTime)
        otd.select_by_visible_text(time)
        sleep(2)

        openGeuest = driver.find_element(By.XPATH,'(//select[contains(@class, "yselect-with-icon search-widget_input--select")])[2]')
        ogd = Select(openGeuest)
        geust_no = guest - 1
        ogd.select_by_index(geust_no)


        sleep(3)