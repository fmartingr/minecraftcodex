from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


###
#   Custom actions
###
def fix_icons(modeladmin, request, queryset):
    for item in queryset:
        try:
            class_name = "%ss" % item.__class__.__name__.lower()
            icon = Texture.objects.get(
                name__exact=item.internal_name,
                type=class_name
            )
            item.main_texture = icon
            item.save()
        except:
            item.main_texture = None
            item.save()

fix_icons.short_description = "Fix icons for the selected items"


def fix_item_data_values(modeladmin, request, queryset):
    for item in queryset:
        if item.internal_id == 0:
            item.internal_id = item.data_value
            if item.__class__.__name__ == 'Item':
                item.data_value += 256
            item.save()
fix_item_data_values.short_description = "Fix data values"


def match_with_minecraftwiki(modeladmin, request, queryset):
    import httplib
    for item in queryset:
        try:
            attr = ModelAttribute.objects.get(
                content_type=ContentType.objects.get_for_model(item),
                object_id=item.pk,
                key='minecraftwiki'
            )
        except:
            name = item.name().replace(' ', '_')
            conn = httplib.HTTPConnection('www.minecraftwiki.net')
            conn.request("HEAD", '/wiki/%s' % name)
            response = conn.getresponse()
            if response.status == 200:
                url = 'http://www.minecraftwiki.net/wiki/%s' % name
                attr = ModelAttribute(
                    content_type=ContentType.objects.get_for_model(item),
                    object_id=item.pk,
                    key='minecraftwiki',
                    value=url
                )
                attr.save()

match_with_minecraftwiki.short_description = "Match MinecraftWiki URLs"


###
#   ATTRIBUTE
###
class ModelAttribute(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    key = models.CharField(max_length=128)
    value = models.TextField()

    def __unicode__(self):
        return self.key


class ModelAttributeAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'key', 'value', )
    list_filter = ('key', )
    search_fields = ('key', 'value', )

admin.site.register(ModelAttribute, ModelAttributeAdmin)

class ModelAttributeAdminInline(generic.GenericTabularInline):
    model = ModelAttribute


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
    upcoming = models.BooleanField(default=False)
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


###
#   TEXTURE
###
class Texture(models.Model):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=16, default="items")
    image = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    def get_image(self, size='original'):
        path = self.image
        if size != 'original' and size in [2, 4, 6, 8]:
            path = path.replace('.png', '_x%d.png' % size)
        return path


class TextureAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'image_html', )
    list_display_links = ('name', )
    list_filter = ('type', )
    search_fields = ('name', 'image', )

    def image_html(self, obj):
        return('<img src="/static/textures/%s" height="32" />' % obj.get_image(2))
    image_html.short_description = 'Image'
    image_html.allow_tags = True

admin.site.register(Texture, TextureAdmin)


###
#   ITEM
###
class Item(models.Model):
    version = models.ForeignKey('Version', null=True, blank=True)
    internal_name = models.CharField(max_length=128)
    main_texture = models.ForeignKey('Texture', null=True, blank=True)
    data_value = models.IntegerField()
    internal_id = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name()

    def name(self):
        result = self.internal_name
        try:
            string = LanguageString.objects.get(
                language=14,
                key='item.%s.name' % self.internal_name
            )
            result = string.value
        except:
            pass
        return result


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'internal_id', 'data_value', 'main_texture_html')
    #list_filter = ('type', )
    search_fields = ('internal_name', 'data_value', )

    inlines = [
        ModelAttributeAdminInline
    ]

    actions = [
        fix_icons,
        fix_item_data_values,
        match_with_minecraftwiki
    ]

    def main_texture_html(self, obj):
        if obj.main_texture:
            return(
                '<img src="/static/textures/%s" height="32" />' % \
                    obj.main_texture.get_image(2)
            )
    main_texture_html.short_description = 'Image'
    main_texture_html.allow_tags = True

admin.site.register(Item, ItemAdmin)


###
#   BLOCK
###
class Block(models.Model):
    version = models.ForeignKey('Version', null=True, blank=True)
    internal_name = models.CharField(max_length=128)
    main_texture = models.ForeignKey('Texture', null=True, blank=True)
    data_value = models.IntegerField()
    internal_id = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name()

    def name(self):
        result = self.internal_name
        try:
            string = LanguageString.objects.get(
                language=14,
                key='tile.%s.name' % self.internal_name
            )
            result = string.value
        except:
            pass
        return result


class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'internal_id', 'data_value', 'main_texture_html')
    #list_filter = ('type', )
    search_fields = ('internal_name', 'data_value', )

    inlines = [
        ModelAttributeAdminInline
    ]

    actions = [
        fix_icons,
        fix_item_data_values,
        match_with_minecraftwiki
    ]

    def main_texture_html(self, obj):
        if obj.main_texture:
            return(
                '<img src="/static/textures/%s" height="32" />' % \
                    obj.main_texture.get_image(2)
            )
    main_texture_html.short_description = 'Image'
    main_texture_html.allow_tags = True

admin.site.register(Block, BlockAdmin)


###
#   LANGUAGES
###
class Language(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    region = models.CharField(max_length=32)
    code = models.CharField(max_length=12)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.region)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', )
    list_display_links = ('name', )
    search_fields = ('name', )

admin.site.register(Language, LanguageAdmin)


class LanguageString(models.Model):
    language = models.ForeignKey('Language', db_index=True)
    key = models.CharField(max_length=256, db_index=True)
    value = models.TextField()


class LanguageStringAdmin(admin.ModelAdmin):
    list_display = ('language', 'key', 'value', )
    list_display_links = ('language', 'key', )

    list_filter = ('language', )
    search_fields = ('key', 'value', )

admin.site.register(LanguageString, LanguageStringAdmin)


###
#   ACHIEVEMENTS
###
class Achievement(models.Model):
    internal_name = models.CharField(max_length=128)
    internal_id = models.IntegerField(default=0)

    def name(self):
        result = self.internal_name
        try:
            string = LanguageString.objects.get(
                language=14,
                key='achievement.%s' % self.internal_name
            )
            result = string.value
        except:
            pass
        return result

    def description(self):
        result = self.internal_name
        try:
            string = LanguageString.objects.get(
                language=14,
                key='achievement.%s.desc' % self.internal_name
            )
            result = string.value
        except:
            pass
        return result

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )
    search_fields = ('internalName', 'description', )

admin.site.register(Achievement, AchievementAdmin)
