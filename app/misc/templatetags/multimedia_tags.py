from wagtail.models import Page
from django import template
from django.utils.translation import get_language
from home.models import HomePage
from django.conf import settings
import urllib.parse


register = template.Library()

@register.filter
def get_youtube_video_code(value):
    try:
        params_string = value.split("?")[1]
        params = urllib.parse.parse_qs(params_string)

        if params['v']:
            return params['v'][0]
    except:
        return None
    
    return None
