from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def get_field_verbose_name(instance, field):
    print("init", instance, field)
    instance = ContentType.objects.get(model=instance).model_class()
    return instance._meta.get_field(field).verbose_name
