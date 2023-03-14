import calendar
from datetime import datetime
date = datetime.date.today()   
datetime.timedelta(days=calendar.monthrange(date.year,date.month)[1])