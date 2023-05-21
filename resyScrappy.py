#this is to scrap from resy 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from time import sleep 

driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

driver.get(' https://resy.com/cities/ny/il-fiorista')

sleep(4)

guestDropdown = driver.find_element(By.ID,'party_size')
gdd = Select(guestDropdown)
gdd.select_by_index(3)

sleep(2)

dateDropdown = driver.find_element(By.ID,'DropdownGroup__selector--date--selection').click()

sleep(2)


#print(getMonthYear)

for c in range(12):
    sleep(2)
    getMonthYear = driver.find_element(By.XPATH,"//h2[@class='CalendarMonth__Title']").text
    
    print(getMonthYear)
    monthYear = 'July 2023'
    if monthYear == getMonthYear:    
        print('hello')
        #days = driver.find_element(By.XPATH,f"//td[text()='{myDay}']")
        #days = driver.find_element(By.XPATH,'//*[@id="DayPicker"]/div[3]/div/div[1]/table/tbody/tr[4]/td[5]')
        days = driver.find_elements(By.XPATH,'//button[@aria-label="July 9, 2023."]')
        print('i reached here')
        

        for i in days:
            print('boo')
            print(i.get_attribute('aria-label'))
            if i.get_attribute('aria-label')==('July 9, 2023.'):
                i.click()
                print('clicked')
                sleep(5)
                print("man")
                break
        break    
    else:
        nextBtn = driver.find_element(By.XPATH,'//*[@id="DayPicker"]/div[2]/button/i')
        nextBtn.click()
        print('btn clicked')
        sleep(2)

sleep(2)

reseveationsTime = driver.find_elements(By.XPATH,'//*[@id="page-content"]/venue-page/div/div[1]/div[1]/div[2]/div[2]/div')

for i in reseveationsTime:
    print(i.text)