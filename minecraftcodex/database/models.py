from django.db import models
from django.contrib import admin

###
#   MOD
###
class Mod(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        app_label = 'database'
        ordering = ['name']


class ModAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_version', 'url_html', )
    list_display_links = ('name', )

    list_filter = ('name', )
    search_fields = ['name', 'url', ]
    ordering = ('name', )

    def last_version(self, obj):
        return obj.version_set.all().\
            order_by('-date')[0].version_number

    def url_html(self, obj):
        if obj.url != '':
            return ('<a href="%s">%s</a>' % (obj.url, obj.url))
        else:
            return "--"
    url_html.short_description = 'URL'
    url_html.allow_tags = True

admin.site.register(Mod, ModAdmin)

###
#   JARFILE
###
class JarFile(models.Model):
    version = models.ForeignKey('Version')
    description = models.CharField(max_length=256, default='client')
    url = models.URLField()

    class Meta:
        app_label = 'database'


class JarFileAdmin(admin.ModelAdmin):
    list_display = ('version', 'description', 'url_html', )

    def url_html(self, obj):
        if obj.url != '':
            return ('<a href="%s">%s</a>' % (obj.url, obj.url))
        else:
            return "--"
    url_html.short_description = 'URL'
    url_html.allow_tags = True

admin.site.register(JarFile, JarFileAdmin)

###
#   VERSION
###
class Version(models.Model):
    mod = models.ForeignKey('Mod')
    version_number = models.CharField(
        max_length=256,
        default='0.1.0'
    )
    status = models.CharField(max_length=10,
        blank=True,
        default='release'
    )
    snapshot = models.BooleanField(default=False)
    date = models.DateField()
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=128,
        blank=True,
        null=False
    )
    changelog = models.TextField('changelog')

    def get_jarfiles(self):
        self.jarfiles = JarFile.objects.filter(version=self)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.get_jarfiles()

    def __unicode__(self):
        return "%s %s" % (
            self.mod,
            self.version_number
        )

    class Meta:
        app_label = 'database'
        ordering = ['date']


class VersionAdmin(admin.ModelAdmin):
    list_display = ('mod', 'status', 'snapshot', 'version_number', 'name', 'url_html', 'date')
    list_display_links = ('version_number',)
    list_filter = ('mod', 'date', 'status')
    search_fields = ['version_number', 'name', 'changelog']
    ordering = ('-date', '-version_number')

    def url_html(self, obj):
        if obj.url:
            return ('<a href="%s">%s</a>' % (obj.url, obj.url))
        else:
            return "--"
    url_html.short_description = 'URL'
    url_html.allow_tags = True

admin.site.register(Version, VersionAdmin)
