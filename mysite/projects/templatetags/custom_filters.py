from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """Splits the string by the given key."""
    return value.split(key)

@register.filter(name='trim')
def trim(value):
    """Trims whitespace from both ends of a string."""
    return value.strip()