from time import sleep
from datetime import datetime, timedelta
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

class Sevenrooms:
    monthNum = datetime.now().month
    year = str(datetime.now().year)
    month = calendar.month_name[monthNum]
    theDay = datetime.now().day
    day = str(theDay)
    monthYear = month + ' ' + year
    monthDayYear = month + day + ',' + year
    current_time = datetime.now()
    rounded_time = current_time + timedelta(minutes=30 - current_time.minute % 30)
    rounded_time = rounded_time.replace(second=0, microsecond=0).strftime("%I:%M %p").lstrip("0").lower()

    driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

    def run(self, path, time=rounded_time, day=day, guest=3, month_year=monthYear):
        self.driver.get(path)
        self.driver.maximize_window()

        try:
            sleep(2)
            reservationTables = self.driver.find_element(By.ID, 'dining-widget-app')
        except NoSuchElementException:
            self.driver.close()
            raise NoSuchElementException('Reservation table not found')

        if not reservationTables:
            self.driver.close()
            raise NoSuchElementException('Reservation table not available')
        else:
            self.driver.find_element(By.XPATH, '//*[@id="sr-search-initial-comp"]/div').click()
            sleep(2)

            for i in range(12):
                monthYear = month_year
                getMonthYear = self.driver.find_element(By.XPATH,
                                                       '//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/div/span[1]').text
                if monthYear == getMonthYear:
                    selectedDay = str(day)
                    getDay = self.driver.find_element(By.XPATH, f"//td[text()='{selectedDay}']")
                    getDay.click()
                    break
                else:
                    arrowbtn = self.driver.find_element(By.XPATH,
                                                        '//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/button[2]').click()
                    print('arrow clicked')
            sleep(2)

            self.driver.find_element(By.XPATH,
                                     '//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[2]/div/div').click()
            numberOfGuest = str(guest)
            self.driver.find_element(By.XPATH, f"//button[text()='{numberOfGuest}']").click()
            sleep(2)

            self.driver.find_element(By.XPATH,
                                     '//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[3]/div/div').click()
            selectedTime = time
            self.driver.find_element(By.XPATH, f"//button[text()='{selectedTime}']").click()
            sleep(2)

            self.driver.find_element(By.XPATH,
                                     '//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[4]/div/button').click()
            sleep(8)

            getResult = self.driver.find_elements(
                By.XPATH, '//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[3]')

            fullData = []

            if len(getResult) > 0:
                for a in getResult:
                    data = a.text
                    times = data.split('\n')
                    for time_slot in times:
                        if ':' in time_slot:
                            time_parts = time_slot.split()
                            hour, minute = time_parts[0].split(':')
                            period = time_parts[1]
                            if period.lower() == 'pm' and int(hour) != 12:
                                hour = str(int(hour) + 12)
                            current_datetime = datetime.now()
                            reservation_datetime = datetime(
                                year=current_datetime.year,
                                month=current_datetime.month,
                                day=current_datetime.day,
                                hour=int(hour),
                                minute=int(minute)
                            )
                            reservation_dict = {
                                'datetime': reservation_datetime,
                            }
                            fullData.append(reservation_dict)
                    break



                print('day available for reservation:', day + ', ' + month_year)
                print('time available for reservations:', fullData)
            else:
                self.theDay = self.theDay + 1
                day = str(self.theDay)
                self.run(day=day, path=path, time=time)
                self.driver.refresh()


o = Sevenrooms()

o.run(path='https://www.sevenrooms.com/reservations/jams')