#this script is to scrape from open table website. 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from time import sleep 

driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

driver.get('https://www.opentable.com/restref/client/?rid=97249')

guestDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[1]/div/select')
timeDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[3]/div/select')
dateDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[2]')
findTableButton = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/button')

dateDropdown.click()

sleep(2)

monthYear = 'July 2023'
found_month_year = False

while not found_month_year:
    getMonthYear = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/div[1]').text
    print(getMonthYear)
    print(monthYear)
    sleep(2)
    if monthYear == getMonthYear:
        myDay = '20'    
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


gdd.select_by_index(9)
tdd.select_by_visible_text('9:30 pm')

findTableButton.click()

sleep(3)

getAvailTime = driver.find_elements(By.XPATH,'//*[@id="panel-home"]/div[1]/div/ul')

print(getAvailTime)

for a in getAvailTime:
    print(a.text)

sleep(5)