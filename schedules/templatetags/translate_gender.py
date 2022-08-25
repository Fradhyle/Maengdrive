from django import template

register = template.Library()


@register.filter
def translate_gender(object):
    if object == "M":
        return "남성"
    elif object == "F":
        return "여성"


@register.filter
def translate_gender_short(object):
    if object == "M":
        return "남"
    elif object == "F":
        return "여"
