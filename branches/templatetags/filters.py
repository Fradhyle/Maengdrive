from django import template

register = template.Library()


@register.filter
def get_attr(object, attr):
    return getattr(object, attr)


@register.filter
def get_object_name(object):
    return object._meta.object_name


@register.filter
def get_model_name(object):
    return object._meta.model_name
