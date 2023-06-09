from time import sleep
from datetime import datetime
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
driver.get("https://www.yelp.com/reservations/blue-india-atlanta")

sleep(2)
openCalendar = driver.find_element(By.XPATH,'//div[contains(@class, "DayPickerInput")]').click()

foundMonthYear = False
sleep(2)

while not foundMonthYear:
    sleep(2)
    monthYear = 'May 2023'
    getMonthYear = driver.find_element(By.XPATH,'//*[@id="react-mount-search-widget"]/div/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div').text

    if monthYear == getMonthYear: 
        theDay = '22'
        getDay = driver.find_element(By.XPATH,'//p[text()="22"]').click()
        foundMonthYear = True
        sleep(2)
    else:
        nextBtn = driver.find_element(By.XPATH, '//span[contains(@class, "DayPicker-NavButton DayPicker-NavButton--next")]')
        nextBtn.click()
        sleep(2)

openTime = driver.find_element(By.XPATH,'(//select[contains(@class, "yselect-with-icon search-widget_input--select")])[1]')
otd = Select(openTime)
otd.select_by_visible_text('11:30 am')
sleep(2)

openGeuest = driver.find_element(By.XPATH,'(//select[contains(@class, "yselect-with-icon search-widget_input--select")])[2]')
ogd = Select(openGeuest)
ogd.select_by_index(0)



sleep(3)

