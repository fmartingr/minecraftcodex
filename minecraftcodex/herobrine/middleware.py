from django.utils.html import strip_spaces_between_tags
from django.conf import settings
import re


class HTMLCleanerMiddleware(object):
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            content = response.content
            if not settings.DEBUG:
                # Remove spaces
                content = strip_spaces_between_tags(content)
                # Remove HTML comments
                exp = re.compile('\<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)\>')
                content = exp.sub('', content)
            response.content = content
        return response
