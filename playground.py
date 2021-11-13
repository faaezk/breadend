from datetime import datetime
import pytz

now = datetime.now()

tz = pytz.timezone('Australia/Melbourne')
melb_now = datetime.now(tz)



#print(now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S"))
#print(melb_now.strftime("%d/%m/%Y") + " at " + melb_now.strftime("%H:%M:%S"))