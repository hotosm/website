from django import template

register = template.Library()


@register.filter
def title_case(value):
    return value.title()
