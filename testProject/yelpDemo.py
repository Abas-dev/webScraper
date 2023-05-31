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

class Yelp:

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
    if rounded_time.endswith('am'):
        rounded_time = rounded_time[:-2] + 'pm'

    def run(self, path, time=rounded_time, day=day, guest=3, month_year=monthYear):
        driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
        driver.get(path)
        driver.maximize_window()
        sleep(2)

        try:
            reservationTables = driver.find_element(By.ID, 'react-mount-search-widget')
        except NoSuchElementException:
            driver.close()
            raise NoSuchElementException('Reservation table not found')

        if not reservationTables:
            driver.close()
            raise NoSuchElementException('Reservation table not available')
        else:
            driver.find_element(By.XPATH, '//div[contains(@class, "DayPickerInput")]').click()

            foundMonthYear = False
            sleep(2)

            while not foundMonthYear:
                sleep(2)
                monthYear = month_year
                getMonthYear = driver.find_element(By.XPATH, '//*[@id="react-mount-search-widget"]/div/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div').text

                if monthYear == getMonthYear: 
                    theDay = day
                    driver.find_element(By.XPATH, f'//p[text()="{theDay}"]').click()
                    foundMonthYear = True
                    sleep(2)
                else:
                    nextBtn = driver.find_element(By.XPATH, '//span[contains(@class, "DayPicker-NavButton DayPicker-NavButton--next")]')
                    nextBtn.click()
                    sleep(2)

            openTime = driver.find_element(By.XPATH, '(//select[contains(@class, "yselect-with-icon search-widget_input--select")])[1]')
            otd = Select(openTime)
            otd.select_by_visible_text(time)
            sleep(2)

            openGuest = driver.find_element(By.XPATH, '(//select[contains(@class, "yselect-with-icon search-widget_input--select")])[2]')
            ogd = Select(openGuest)
            guest_no = guest - 1
            ogd.select_by_index(guest_no)
            
            sleep(3)

            availTime = driver.find_elements(By.XPATH, '//*[@id="react-mount-search-widget"]/div/div/div[2]/div/div[1]/ul/li/div/div/div[2]')

            fullData = []

            if len(availTime) > 0:
                for a in availTime:
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
                    break
                    
                print('day availabe for resevation: ', day + ', ' + month_year)
                print('time available for reservations: ', fullData)
            else:
                self.theDay = self.theDay + 1 
                day = str(self.theDay)
                self.run(day=day, path=path, time=time)
                driver.refresh()

            sleep(3)


h = Yelp()

h.run(path='https://www.yelp.com/reservations/blue-india-atlanta')