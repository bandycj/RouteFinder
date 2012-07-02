import os
import urllib

from datetime import datetime
from django.conf import settings
from lxml.html import parse, etree
from lxml.cssselect import CSSSelector

from RouteFinder.utils import render_to_response
from RouteFinder.search.models import Airport, Flight
from RouteFinder.schedule.processor import getSchedule, getTimezoneForAirport

GEOCODE_URL = "http://www.mapquestapi.com/geocoding/v1/address?key=Fmjtd%7Cluua2gu2n0%2Caw%3Do5-hfzs1&mapData=nadb,1547&outFormat=xml&location="
TIMEZONE_URL = "http://www.earthtools.org/timezone/%s/%s"

CITY_ROWS = CSSSelector('td.city')
STATION_ID_DIV = CSSSelector('div.stationID')
AIRPORT_NAME_DIV = CSSSelector('div.airport_name')

def index(request):
    return render_to_response('schedule/index.html')


def airports(request):
    """

    """
    url = "http://www.southwest.com/html/air/airport-information.html"
    doc = parse(url).getroot()
    static_files = getattr(settings, 'STATIC_URL')
    airportsDat = urllib.urlopen("%s/airports.dat" % static_files)
    for row in CITY_ROWS(doc):
#        try:
        iataCode = STATION_ID_DIV(row)[0].text
        name = AIRPORT_NAME_DIV(row)[0].text
        for line in airportsDat.read():
            split = line.split(",")
            currentIata = split[4]
            offset = split[9]
            dst = split[10]
            if currentIata == iataCode:
                print "%s : %s : %s" % (currentIata, offset,dst)
#        cityName = name[:name.index(" - ")].replace(" ", "%20")
#        url = GEOCODE_URL + cityName
#        search = etree.fromstring(urllib.urlopen(url).read())
#        lat = search.xpath("//lat")[0].text
#        lng = search.xpath("//lng")[0].text
#        print TIMEZONE_URL % (lat,lng)
#        print "%s : %s" % (iataCode, name)
#
#        airport = Airport.objects.get_or_create(iataCode=iataCode, name=name)
#        airport.save()
#        except:
#            continue


    return render_to_response('schedule/airports.html', {
        'airports': Airport.objects.all()
    })


def scheduleCities(request):
    airport_list = Airport.objects.all().order_by('iataCode')
    return render_to_response('schedule/schedule_form.html', {
        'airport_list': airport_list
    })


def scheduleForm(request, iataCode=None):
    return render_to_response('schedule/schedule_form.html', {
        'iataCode': iataCode,
        })


def updateSchedule(request, iataCode=None):
    if request.method == 'POST':
        data = getSchedule(iataCode)
        for flight in data:
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
    return render_to_response('schedule/update_result.html', {
        'data': data
    })