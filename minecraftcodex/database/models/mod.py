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
    list_display = ('name', 'last_version', 'url', )
    list_display_links = ('name', )

    list_filter = ('name', )
    search_fields = ['name', 'url', ]
    ordering = ('name', )

    def last_version(self, obj):
        return '0.0.0'

admin.site.register(Mod, ModAdmin)
