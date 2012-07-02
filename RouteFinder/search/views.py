from RouteFinder.search.models import Airport, Flight
from RouteFinder.utils import render_to_response

MAX_HOPS = 3

def origins(request):
    airport_list = Airport.objects.all().order_by('iataCode')

    return render_to_response('search/search.html', {
        'page_title': "Origin",
        'airport_list': airport_list,
        })


def destinations(request, origin=None):
    airport_list = Airport.objects.all().order_by('iataCode')

    return render_to_response('search/search.html', {
        'page_title': "Destination",
        'origin': origin,
        'airport_list': airport_list,
        })


def final(request, origin=None, destination=None):
    return render_to_response('search/search.html', {
        'page_title': "Search",
        'origin': origin,
        'destination': destination,
        'max_hops': MAX_HOPS,
        })


def result(request, origin=None, destination=None):
    if request.method == 'POST':
        o = Airport.objects.get(pk=origin)
        d = Airport.objects.get(pk=destination)
        flights = Flight.objects.filter(origin=o, destination=d)

        return render_to_response('search/result.html', {
            'flights': flights
        })

    return render_to_response('search/search.html', {
        'page_title': "Search",
        'origin': origin,
        'destination': destination,
        'max_hops': MAX_HOPS
    })
