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
    def run(self, path, time=None, month_year=None, day=None, guest=3):
        if time is None:
            current_time = datetime.now()
            rounded_time = current_time + timedelta(minutes=30 - current_time.minute % 30)
            rounded_time = rounded_time.replace(second=0, microsecond=0).strftime("%I:%M %p").lstrip("0").lower()
        else:
            rounded_time = time

        monthNum = datetime.now().month
        year = str(datetime.now().year)
        month = calendar.month_name[monthNum]
        theDay = datetime.now().day
        day = str(theDay) if day is None else day
        monthYear = month + ' ' + year if month_year is None else month_year
        monthDayYear = month + day + ',' + year

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
            guestDropdown = driver.find_element(By.XPATH, '//*[@id="DtpForm1"]/div/div[1]/div/select')
            timeDropdown = driver.find_element(By.XPATH, '//*[@id="DtpForm1"]/div/div[3]/div/select')
            dateDropdown = driver.find_element(By.XPATH, '//*[@id="DtpForm1"]/div/div[2]')
            findTableButton = driver.find_element(By.XPATH, '//*[@id="DtpForm1"]/div/button')

            dateDropdown.click()
            sleep(2)

            monthYear = month_year
            found_month_year = False

            while not found_month_year:
                getMonthYear = driver.find_element(By.XPATH,
                                                  '//*[@id="DtpForm1"]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/div[1]').text
                if monthYear == getMonthYear:
                    myDay = str(day)
                    days = driver.find_element(By.XPATH, f"//div[text()='{myDay}']")
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

            tdd.select_by_visible_text(rounded_time)

            findTableButton.click()

            sleep(3)

            getAvailTime = driver.find_elements(By.XPATH, '//*[@id="panel-home"]/div[1]/div/ul')

            print(getAvailTime)

            fullData = []

            if len(getAvailTime) > 0:
                for a in getAvailTime:
                    data = a.text
                    times = data.split('\n')
                    fullData.extend(times)
                    break

                print('day available for reservation:', day + ', ' + month_year)
                print('time available for reservations:', fullData)
            else:
                # Change AM to PM if no available slots
                if rounded_time.endswith('am'):
                    time = rounded_time.replace('am', 'pm')
                else:
                    time = rounded_time.replace('pm', 'am')
                self.run(day=day, path=path, time=time)
                # driver.refresh()

            sleep(5)
