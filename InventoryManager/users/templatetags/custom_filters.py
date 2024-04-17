from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def add_attributes(field, attrs_string):
    attrs = {}
    for item in attrs_string.split(','):
        key, value = item.split(':')
        attrs[key.strip()] = value.strip()
    return field.as_widget(attrs=attrs)


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
