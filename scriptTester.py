from mainProject.resy import Resy
from mainProject.sevenrooms import Sevenrooms
from mainProject.yelp import Yelp
from mainProject.opentable import Opentable

open = Yelp()
 
open.run(' https://www.yelp.com/reservations/blue-india-atlanta',time='9:00 pm', guest=8)