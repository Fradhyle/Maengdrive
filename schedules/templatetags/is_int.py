from django import template

register = template.Library()


@register.filter
def is_int(object):
    return isinstance(object, int)
