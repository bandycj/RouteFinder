from django.db import models


class Airport(models.Model):
    iataCode = models.TextField(max_length=3, primary_key=True, db_index=True)
    name = models.TextField(max_length=32)

    def __unicode__(self):
        return self.iataCode


class Flight(models.Model):
    origin = models.ForeignKey(Airport, related_name="origin", on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, related_name="destination", on_delete=models.CASCADE)
    flightNum = models.IntegerField()
    fromDate = models.DateTimeField(auto_now=False)
    toDate = models.DateTimeField(auto_now=False)
    ska = models.DateTimeField(auto_now=False)
    skd = models.DateTimeField(auto_now=False)

    def __unicode__(self):
        return self.origin.iataCode + self.destination.iataCode + str(self.flightNum) + str(fromDate) + str(toDate)

