import time
from datetime import datetime

from_date = '2020-10-10'
to_date = '2020-12-12'


from_date = time.mktime(datetime.strptime(
    from_date, '%Y-%m-%d').timetuple()) / 100
to_date = time.mktime(datetime.strptime(to_date, '%Y-%m-%d').timetuple())

print(from_date)
print(type(from_date))
