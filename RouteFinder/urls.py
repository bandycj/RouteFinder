from django.conf.urls import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^$', 'RouteFinder.views.index', name='home'),
    url(r'^search/$', 'RouteFinder.search.views.origins'),
    url(r'^search/(?P<origin>[A-Z]{3})/$', 'RouteFinder.search.views.destinations'),
    url(r'^search/(?P<origin>[A-Z]{3})/(?P<destination>[A-Z]{3})/$', 'RouteFinder.search.views.final'),
    url(r'^search/(?P<origin>[A-Z]{3})/(?P<destination>[A-Z]{3})/result$', 'RouteFinder.search.views.result'),
    url(r'^schedule/$', 'RouteFinder.schedule.views.index'),
    url(r'^schedule/airports$', 'RouteFinder.schedule.views.airports'),
    url(r'^schedule/scheduleCities$', 'RouteFinder.schedule.views.scheduleCities'),
    url(r'^schedule/scheduleForm/(?P<iataCode>[A-Z]{3})/$', 'RouteFinder.schedule.views.scheduleForm'),
    url(r'^schedule/updateSchedule/(?P<iataCode>[A-Z]{3})/$', 'RouteFinder.schedule.views.updateSchedule'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
