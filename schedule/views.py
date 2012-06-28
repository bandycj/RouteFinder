from datetime import datetime
from lxml.html import parse
from lxml.cssselect import CSSSelector

from RouteFinder.utils import render_to_response
from search.models import Airport, Flight
from processor import getSchedule

CITY_ROWS = CSSSelector('td.city')
STATION_ID_DIV = CSSSelector('div.stationID')
AIRPORT_NAME_DIV = CSSSelector('div.airport_name')

def index(request):
    return render_to_response('schedule/index.html')


def airports(request):
    url = "http://www.southwest.com/html/air/airport-information.html"
    doc = parse(url).getroot()

    for row in CITY_ROWS(doc):
        try:
            iataCode = STATION_ID_DIV(row)[0].text
            name = AIRPORT_NAME_DIV(row)[0].text
            airport = Airport.objects.get_or_create(iataCode=iataCode, name=name)
            airport.save()
        except:
            continue
        print "%s : %s" % (iataCode, name)

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
        date = request.POST['date']
        data = getSchedule(iataCode, date)
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

    template = env.get_template(filename)
    rendered = template.render(**context)
    return HttpResponse(rendered, mimetype=mimetype)
