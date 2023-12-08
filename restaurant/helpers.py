""" 
takes the opening hours data and the current date and time as inputs and returns
a boolean value indicating whether the restaurant is open or closed.
"""

from datetime import datetime

def is_restaurant_open(opening_hours):
    now = datetime.now().time()
    current_weekday = datetime.now().weekday()

    for opening_hour in opening_hours:
        if opening_hour.weekday -1 == current_weekday:
            if opening_hour.open_time <= now <= opening_hour.close_time:
                return True

    return False