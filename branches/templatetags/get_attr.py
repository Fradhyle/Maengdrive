from django import template

register = template.Library()


@register.filter
def get_attr(object, attr):
    return getattr(object, attr)
