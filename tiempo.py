from datetime import datetime
from zoneinfo import ZoneInfo

ahora = datetime.now(ZoneInfo("America/Bogota"))
print(ahora)
print(datetime.now())
