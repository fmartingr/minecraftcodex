from django.db import models
from django.contrib import admin
import datetime
from django.utils.timezone import utc


# Create your models here.
class BlogEntry(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    slug = models.SlugField(max_length=128)

    class Meta:
        app_label = 'blog'
        ordering = ['-date']


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', )
    list_display_links = ('title', )

    list_filter = ('date', )
    search_fields = ('title', 'content', )

    prepopulated_fields = {"slug": ("title",)}

    class Media:
        css = {
            "all": ("lib/redactor.css",)
        }
        js = ("lib/redactor.js",)

admin.site.register(BlogEntry, BlogEntryAdmin)
