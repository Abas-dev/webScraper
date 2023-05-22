from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from time import sleep 

driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

driver.get('https://www.sevenrooms.com/reservations/jams')


opentDateField = driver.find_element(By.XPATH,'//*[@id="sr-search-initial-comp"]/div').click()

sleep(2)

for i in range(12):
    monthYear = 'June 2023'
    getMonthYear = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/div/span[1]').text
    if monthYear == getMonthYear:
        day = '27'
        getDay = driver.find_element(By.XPATH,f"//td[text()='{day}']")
        getDay.click()
        break
    else:
        arrowbtn = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/button[2]').click()
        print('arrow clicked')
sleep(2)

openGuestField = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[2]/div/div').click()
numberOfGuest = '4'
getGuestNumber = driver.find_element(By.XPATH,f"//button[text()='{numberOfGuest}']").click()

sleep(2)

openTimeField = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[3]/div/div').click()
selectedTime = '10:45 am'
getTime = driver.find_element(By.XPATH,f"//button[text()='{selectedTime}']").click()

sleep(2)    

bookBtn = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[4]/div/button').click()
sleep(8)

getResult = driver.find_elements(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[3]')

for i in getResult:
    print(i.text)