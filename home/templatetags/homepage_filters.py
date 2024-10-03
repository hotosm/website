from django import template
import numbers

register = template.Library()

@register.filter
def prettify_number(value):
    if not isinstance(value, numbers.Number):
        return value
    
    if value >= 1000000:
        value = "{value:.1f}M".format(value=value/1000000)
    elif value >= 1000:
        value = "{value:.1f}K".format(value=value/1000)
    
    return value