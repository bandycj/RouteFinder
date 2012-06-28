from processor import getSchedule
from datetime import datetime

startTime = datetime.now()

result = getSchedule("BOS", "06/26/2012")
print "Results: " + str(len(result))

#    lines = sort(dumpPdf(link))
#    for line in lines:
#        print "%s %s %s" % (line['origin'], line['destination'], line['flightNum'])
#print "Results: %s" % len(lines)
print(datetime.now() - startTime)
