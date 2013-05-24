from django.conf.urls import patterns, include, url
from django.http import HttpResponse, HttpResponseRedirect

# Admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'herobrine.views.home', name='home'),
    # url(r'^herobrine/', include('herobrine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^management/', include(admin.site.urls)),
    url(r'^$', 'database.views.home'),
    # Static
    url(r'^about/', 'database.views.about'),
    # Database
    url(r'^versions/(?P<version>[a-z0-9\.\_]+)/', 'database.views.version', name='version_release'),
    url(r'^versions/(?P<status>[a-z]+)\-(?P<version>[a-z0-9\.\_]+)/', 'database.views.version', name='version'),
    url(r'^versions/', 'database.views.versions'),
    # Robots
    (r'^robots\.txt$', lambda r: HttpResponse("", mimetype="text/plain")),
    # Favicon
    (r'^favicon\.ico$', lambda r: HttpResponseRedirect('/static/favicon.ico')),
)
