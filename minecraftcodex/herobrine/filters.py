from jingo import register
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode
from django.conf import settings
from pytz import timezone
import pytz


@register.filter
def dt(t, fmt=None):
    """Call ``datetime.strftime`` with the given format string."""
    tz = timezone(settings.TIME_ZONE)
    if fmt is None:
        fmt = _('%B %e, %Y')
    return smart_unicode(tz.normalize(t).strftime(fmt)) if t else u''
