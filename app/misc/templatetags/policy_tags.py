from wagtail.models import Page
from django import template
from django.utils.translation import get_language
from home.models import HomePage
from django.conf import settings
from app.misc.models import GeneralPolicyOwnerPage

register = template.Library()

@register.simple_tag(takes_context=True)
def get_internal_policy_links(context):
    current_page = context.get('self')

    if current_page is None:
        return None

    owners = GeneralPolicyOwnerPage.objects.live().filter(locale=current_page.locale)

    if len(owners):
        owner = owners[0]
        return owner.get_children()

    return None