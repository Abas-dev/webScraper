from time import sleep
from datetime import datetime, timedelta
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager    
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

class Opentable:
    def __init__(self):
        self.monthNum = datetime.now().month
        self.year = str(datetime.now().year)
        self.month = calendar.month_name[self.monthNum]
        self.theDay = datetime.now().day
        self.day = str(self.theDay)
        self.monthYear = self.month + ' ' + self.year
        self.monthDayYear = self.month + self.day + ',' + self.year
        self.current_time = datetime.now()
        self.rounded_time = self.current_time + timedelta(minutes=30 - self.current_time.minute % 30)
        self.rounded_time = self.rounded_time.replace(second=0, microsecond=0).strftime("%I:%M %p").lstrip("0").lower()

    def run(self, path, time=None, month_year=None, day=None, guest=3):
        if time is None:
            time = self.rounded_time
        if month_year is None:
            month_year = self.monthYear
        if day is None:
            day = self.day

        driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
        driver.get(path)
        driver.maximize_window()
        
        try:
            sleep(2)
            reservationTables = driver.find_elements(By.XPATH, '//*[@id="panel-home"]')
        except NoSuchElementException:
            driver.close()
            raise NoSuchElementException('Reservation table not found')

        if not reservationTables:
            driver.close()
            raise NoSuchElementException('Reservation table not available')
        else:
            guestDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[1]/div/select')
            timeDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[3]/div/select')
            dateDropdown = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[2]')
            findTableButton = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/button')

            dateDropdown.click()
            sleep(2)

            found_month_year = False

            while not found_month_year:
                getMonthYear = driver.find_element(By.XPATH,'//*[@id="DtpForm1"]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/div[1]').text
                if month_year == getMonthYear:
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
        fullData = []

        if len(getAvailTime) > 0:
            for a in getAvailTime:
                data = a.text
                times = data.split('\n')
                for time_slot in times:
                    if ':' in time_slot:
                        time_parts = time_slot.split()
                        hour, minute = time_parts[0].split(':')
                        period = time_parts[1]
                        if period.lower() == 'pm' and int(hour) != 12:
                            hour = str(int(hour) + 12)
                        elif period.lower() == 'am' and int(hour) == 12:
                            hour = '0'
                        current_datetime = datetime.now()
                        reservation_datetime = datetime(
                            year=current_datetime.year,
                            month=current_datetime.month,
                            day=current_datetime.day,
                            hour=int(hour),
                            minute=int(minute)
                        )
                        reservation_dict = {
                            'datetime': reservation_datetime.strftime("%Y-%m-%d %I:%M %p")
                            
                        }
                        fullData.append(reservation_dict)
                        
            print('day availabe for resevation: ', day + ', ' + month_year)
            print('time available for reservations: ', fullData)
        else:
            self.theDay = self.theDay + 1
            day = str(self.theDay)
            
            if self.rounded_time.endswith('am'):
                self.rounded_time = self.rounded_time[:-2] + 'pm'
                
            self.run(day=day, path=path, time=self.rounded_time)

            
            sleep(5)


opentable = Opentable()
opentable.run('https://www.opentable.com/restref/client/?rid=97249',time='2:00 pm')
