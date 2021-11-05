from datetime import datetime
from ZoneInfo import ZoneInfo

now = datetime.now()

old_hour = now.hour
old_day = now.day

if old_hour > 12:
    now.replace(hour=23)

datetime.datetime.now(ZoneInfo("Europe/Amsterdam"))


print(now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S"))