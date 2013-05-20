from django.conf.urls import patterns, include, url

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
)
