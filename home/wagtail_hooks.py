from wagtail import hooks
from django.core.cache import cache
from home.models import HomePage

@hooks.register('after_edit_page')
def after_edit_page(request, page):
    if isinstance(page, HomePage):
        cache.delete('home_page_stats')
