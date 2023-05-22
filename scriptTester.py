from mainProject.resy import Resy
from mainProject.yelp import Yelp
open = Yelp()
 
open.run('https://www.yelp.com/reservations/blue-india-atlanta','12:00 pm',month_year='June 2023')