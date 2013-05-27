from django.conf.urls import patterns, include, url
from django.http import HttpResponse, HttpResponseRedirect

# Admin
from django.contrib import admin
admin.autodiscover()

# Custom views
handler404 = 'database.views.error404'
handler500 = 'database.views.error500'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'herobrine.views.home', name='home'),
    # url(r'^herobrine/', include('herobrine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^management/', include(admin.site.urls)),
    # Home
    url(r'^$', 'database.views.home', name='homepage'),
    # Static
    url(r'^about/', 'database.views.about', name='aboutpage'),
    # Versions
    url(r'^versions/(?P<version>[A-Za-z0-9\.\_ ]+)/',
        'database.views.version',
        name='version_release'
    ),
    url(r'^versions/(?P<status>[a-z]+)\-(?P<version>[A-Za-z0-9\.\_ ]+)/',
        'database.views.version',
        name='version'
    ),
    url(r'^versions/', 'database.views.versions', name='version_list'),

    # Items
    url(r'^items/', 'database.views.items', name='items_list'),

    # Robots
    (r'^robots\.txt$', lambda r: HttpResponse("", mimetype="text/plain")),

    # Favicon
    (r'^favicon\.ico$', lambda r: HttpResponseRedirect('/static/favicon.ico')),
)
