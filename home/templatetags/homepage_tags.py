from wagtail.models import Page
from django import template
from django.utils.translation import get_language
from home.models import HomePage
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def get_home_page(context):
    current_page = context.get('self')

    if current_page is None:
        return None

    home_page = current_page.get_ancestors(inclusive=True).type(HomePage).first().specific
    
    if not home_page:
        home_page = HomePage.objects.live().filter(locale=context['page'].locale).first().specific

    return home_page


@register.simple_tag(takes_context=True)
def get_navigation(context):
    current_page = context.get('self')

    if current_page is None:
        return None

    navigation = current_page.get_ancestors(inclusive=True).type(HomePage).first().specific.navigation

    return navigation


@register.simple_tag(takes_context=True)
def get_share_links(context):
    current_page = context.get('self')

    if current_page is None:
        return None

    social_share_links = current_page.get_ancestors(inclusive=True).type(HomePage).first().specific.social_share_links

    links = [{"icon": x.value["icon"], "link": str(x.value["link"]).replace("{}", current_page.full_url)} for x in social_share_links]

    return links


@register.simple_tag
def get_mapbox_key():
    return settings.MAPBOX_ACCESS_TOKEN
