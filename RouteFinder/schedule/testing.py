from RouteFinder.schedule.processor import getTimezoneForAirport
from datetime import datetime

startTime = datetime.now()

getTimezoneForAirport("GSP")

print(datetime.now() - startTime)
