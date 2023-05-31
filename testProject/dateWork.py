from time import sleep
from datetime import datetime
import calendar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

class Resy:
    monthNum = datetime.now().month
    year = str(datetime.now().year)
    month = calendar.month_name[monthNum]
    theDay = datetime.now().day
    day = str(theDay)
    monthYear = month + ' ' + year
    monthDayYear = month + day + ',' + year

    driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

    def run(self, path, guest=3, month_year=monthYear, month_day_year=monthDayYear):
        self.driver.get(path)
        self.driver.maximize_window()

        try:
            sleep(2)
            reservationTables = self.driver.find_element(By.XPATH, '//div[@class="VenuePage__Selector-Wrapper"]')
        except NoSuchElementException:
            self.driver.close()
            raise NoSuchElementException('Reservation table not found')

        if not reservationTables:
            self.driver.close()
            raise NoSuchElementException('Reservation table not available')
        else:
            sleep(4)
            guest_no = guest - 1
            guestDropdown = self.driver.find_element(By.ID, 'party_size')
            gdd = Select(guestDropdown)
            gdd.select_by_index(guest_no)

            sleep(2)
            self.driver.find_element(By.ID, 'DropdownGroup__selector--date--selection').click()

            sleep(2)

            for c in range(12):
                sleep(2)
                getMonthYear = self.driver.find_element(By.XPATH, "//h2[@class='CalendarMonth__Title']").text
                print(getMonthYear)
                monthYear = month_year
                if monthYear == getMonthYear:
                    days = self.driver.find_elements(By.XPATH, f'//button[@aria-label="{month_day_year}"]')
                    
                    for i in days:
                        if i.get_attribute('aria-label') == month_day_year:
                            i.click()
                            sleep(5)
                            break
                    break
                else:
                    nextBtn = self.driver.find_element(By.XPATH, '//button[contains(@class, "ResyCalendar__nav_right Button Button--primary Button--circle")]')
                    nextBtn.click()
                    print('btn clicked')
                    sleep(2)

            sleep(2)
            reservationsTime = self.driver.find_elements(By.XPATH, '//*[@id="page-content"]/venue-page/div/div[1]/div[1]/div[2]/div[3]/div')

            fullData = []

            typeBooking = self.driver.find_element(By.CLASS_NAME,'ShiftInventory__shift__title').text
            
            if len(reservationsTime) > 0:
                for a in reservationsTime:
                    data = a.text
                    times = [time for time in data.split('\n') if time != 'Res']
                    fullData.extend(times)

                formatted_data = []
                for time_slot in fullData:
                    if time_slot != 'Notify':
                        time_parts = time_slot.split(':')
                        hour = int(time_parts[0])
                        minute = int(time_parts[1].split()[0])
                        time = datetime(year=int(self.year), month=self.monthNum, day=self.theDay, hour=hour, minute=minute)
                        formatted_data.append({'datetime': time.strftime("%Y-%m-%d %H:%M"), 'am/pm': time_parts[1].split()[1],'type':typeBooking})

                print('Day available for reservation:', self.day + ', ' + self.month)
                print('Time available for reservations:')
                for slot in formatted_data:
                    print('datetime:', slot['datetime'],'am/pm:',slot['am/pm'], 'type:', slot['type'])

                return formatted_data
            else:
                self.theDay = self.theDay + 1
                day = str(self.theDay)
                return self.run(path=path, guest=guest, month_year=month_year, month_day_year=month_day_year)
                self.driver.refresh()



c = Resy()
c.run('https://resy.com/cities/ny/il-fiorista')