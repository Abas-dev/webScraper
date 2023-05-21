from time import sleep
from datetime import datetime
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

class Scapper:
    
    monthNum = datetime.now().month
    year = str(datetime.now().year)
    month = calendar.month_name[monthNum]
    day = str(datetime.now().day)
    monthYear = month +' '+ year
    monthDayYear = month+day+','+year
    current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
    time=current_time

    print(monthYear)
    
    def openTable(self,path,time,month_year=monthYear,day=day,guest=1):
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
        gdd.select_by_index(guest_no)
        
        tdd.select_by_visible_text(time)

        findTableButton.click()

        sleep(3)

        getAvailTime = driver.find_elements(By.XPATH,'//*[@id="panel-home"]/div[1]/div/ul')

        print(getAvailTime)

        for a in getAvailTime:
            print(a.text)

        sleep(5)


    def resy(self,path,guest=1,month_year=monthYear,month_day_year=monthDayYear):
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


    def sevenrooms(self,path,time,day=day,guest=1,month_year=monthYear):
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

        openGuestField = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[2]/div/div').click()
        numberOfGuest = str(guest)
        getGuestNumber = driver.find_element(By.XPATH,f"//button[text()='{numberOfGuest}']").click()

        sleep(2)

        openTimeField = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[3]/div/div').click()
        selectedTime = time
        getTime = driver.find_element(By.XPATH,f"//button[text()='{selectedTime}']").click()

        sleep(2)    

        bookBtn = driver.find_element(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[4]/div/button').click()

        sleep(8)

        getResult = driver.find_elements(By.XPATH,'//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[3]')

        for i in getResult:
            print(i.text)

w = Scapper()
#w.openTable('https://www.opentable.com/restref/client/?rid=97249','July 2023',20,'9:00 pm',8)
#w.resy('https://resy.com/cities/ny/il-fiorista',5,'June 2023','June 7, 2023.')
#w.sevenrooms('https://www.sevenrooms.com/reservations/jams',13,'9:00 pm',5,'July 2023')

#w.openTable('https://www.opentable.com/restref/client/?rid=97249','10:00 pm')
#w.resy('https://resy.com/cities/ny/il-fiorista')
w.sevenrooms('https://www.sevenrooms.com/reservations/jams','9:00 pm')