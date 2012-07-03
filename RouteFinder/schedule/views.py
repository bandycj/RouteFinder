import os
import urllib

from datetime import datetime
from django.conf import settings
from lxml.html import parse, etree
from lxml.cssselect import CSSSelector

from RouteFinder.utils import render_to_response
from RouteFinder.search.models import Airport, Flight
from RouteFinder.schedule.processor import getSchedule, getTimezones

GEOCODE_URL = "http://www.mapquestapi.com/geocoding/v1/address?key=Fmjtd%7Cluua2gu2n0%2Caw%3Do5-hfzs1&mapData=nadb,1547&outFormat=xml&location="
TIMEZONE_URL = "http://www.earthtools.org/timezone/%s/%s"
AIRPORT_URL = "http://www.southwest.com/html/air/airport-information.html"

CITY_ROWS = CSSSelector('td.city')
STATION_ID_DIV = CSSSelector('div.stationID')
AIRPORT_NAME_DIV = CSSSelector('div.airport_name')

def index(request):
    return render_to_response('schedule/index.html')


def update_airports(request):
    doc = parse(AIRPORT_URL).getroot()
#    timezones = getTimezones()
    for row in CITY_ROWS(doc):
        iataCode = STATION_ID_DIV(row)[0].text
        name = AIRPORT_NAME_DIV(row)[0].text
#            tz_offset = timezones[iataCode]['offset']
#            dst = timezones[iataCode]['offset']

        airport = Airport.objects.get_or_create(iataCode=iataCode, name=name)
        print airport
    Airport.objects

    return render_to_response('schedule/schedule_update_airports.html', {
        'airports': Airport.objects.all()
    })


def airports(request):
    airport_list = Airport.objects.all().order_by('iataCode')
    return render_to_response('schedule/schedule_airports.html', {
        'airport_list': airport_list
    })


def form(request, iataCode=None):
    return render_to_response('schedule/schedule_form.html', {
        'iataCode': iataCode,
        })


def update(request, iataCode=None):
    flights = []
    if request.method == 'POST':
        flights = getSchedule(iataCode)
        for flight in flights:
            origin = Airport.objects.get(pk=flight['origin'])
            destination = Airport.objects.get(pk=flight['destination'])
            flightNum = flight['flightNum']
            fromDate = datetime.strptime(flight['fromDate'], "%B %d, %Y")
            toDate = datetime.strptime(flight['toDate'], "%B %d, %Y")
            skd = datetime.strptime(flight['ska'], "%I:%M%p")
            ska = datetime.strptime(flight['skd'], "%I:%M%p")

            f = Flight.objects.get_or_create(
                origin=origin,
                destination=destination,
                flightNum=flightNum,
                fromDate=fromDate,
                toDate=toDate,
                skd=skd,
                ska=ska
            )
    return render_to_response('schedule/schedule_update.html', {
        'flights': flights
    })

def update_timezones(request):
    timezones = updateTimezones()
    return render_to_response('schedule/schedule_update_timezones.html', {
        'timezones': timezones
    })