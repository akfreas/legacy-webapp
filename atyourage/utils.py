from datetime import datetime
from math import floor
def get_age(year, month, day):

    now = datetime.now()
    total_months = year*12 + month - 1;        # total months for birthdate.
    total_months_now = now.year*12 + now.month - 1;   # total months for Now.
    delta_months = total_months_now - total_months;              # delta months.    
    if(now.day >= day):
        return [int(floor(delta_months/12)), delta_months%12, now.day-day];
    else:
        total_years = floor(total_months_now/12)
        print total_months_now%12+1
        thetime = datetime(now.year, total_months_now%12+1, day, 0, 0, 0).ctime()
        print thetime
        delta_months-=1
        total_months_now-=1
        return [floor(delta_months/12), delta_months%12, thetime/60/60/24];
