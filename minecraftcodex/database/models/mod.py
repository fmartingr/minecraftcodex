from django.db import models
from django.contrib import admin


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
