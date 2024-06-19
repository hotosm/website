from wagtail.models import Page
from django import template
from django.utils.translation import get_language
from home.models import HomePage

register = template.Library()

@register.simple_tag(takes_context=True)
def get_home_page(context):
    current_page = context.get('self')

    if current_page is None:
        return None

    home_page = current_page.get_ancestors(inclusive=True).type(HomePage).first().specific

    return home_page


@register.simple_tag(takes_context=True)
def get_navigation(context):
    current_page = context.get('self')

    if current_page is None:
        return None

    navigation = current_page.get_ancestors(inclusive=True).type(HomePage).first().specific.navigation

    return navigation
