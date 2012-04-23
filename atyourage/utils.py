from datetime import datetime
from math import floor

def get_age(year, month, day):


     now = datetime.now()
     birthday = datetime(year, month, day)

     delta = now - birthday
     days_delta = float(delta.days)

     years_old = days_delta / 365.25
     months_old = (years_old * 12) % 12
     months_old_delta = years_old * 12
     days_old = now.day - birthday.day 
     if days_old < 0:
         days_old = abs(days_old)
         days_old = days_old + now.day
     print months_old - floor(months_old)
     print years_old, months_old, days_old
     delta_list = map(int, map(floor, [years_old, months_old, days_old]))

     ddict = {"years": delta_list[0], "months": delta_list[1], "days": delta_list[2]}
     return ddict 
