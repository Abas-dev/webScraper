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
    driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

    def run(self, path, time=None, day=None, guest=3):
        monthNum = datetime.now().month
        year = str(datetime.now().year)
        month = calendar.month_name[monthNum]
        theDay = datetime.now().day
        if day is None:
            day = str(theDay)
        monthYear = month + ' ' + year
        monthDayYear = month + day + ', ' + year

        if time is None:
            current_time = datetime.now()
            rounded_time = current_time + timedelta(minutes=30 - current_time.minute % 30)
            rounded_time = rounded_time.replace(second=0, microsecond=0).strftime("%I:%M %p").lstrip("0").lower()
        else:
            rounded_time = time

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
            self.driver.find_element(By.XPATH, f"//button[text()='{rounded_time}']").click()

            sleep(2)

            self.driver.find_element(By.XPATH,
                                     '//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div[4]/div/button').click()

            sleep(8)

            getResult = self.driver.find_elements(By.XPATH,
                                                  '//*[@id="dining-widget-app"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[3]')

            fullData = []

            if len(getResult) > 0:
                for a in getResult:
                    data = a.text
                    times = data.split('\n')
                    fullData.extend(times)
                    break

                print('Day available for reservation:', day + ', ' + monthYear)
                print('Time available for reservations:')
                formatted_data = []
                for slot in fullData:
                    
                    time_parts = slot.split(' ')[0].split(':')
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    time = datetime(year=int(year), month=monthNum, day=theDay, hour=hour, minute=minute)
                    type = slot.split(' ')[1]
                    formatted_data.append({'datetime': f"datetime(year={time.year}, month={time.month}, day={time.day}, hour={time.hour}, minutes={time.minute})", 'type': type})

                return formatted_data
            else:
                self.theDay = self.theDay + 1
                day = str(self.theDay)
                return self.run(day=day, path=path, time=time)
                self.driver.refresh()


# Example usage
sevenrooms = Sevenrooms()
time_slots = sevenrooms.run('https://www.sevenrooms.com/reservations/jams',time= '10:00 pm')
print(time_slots)
