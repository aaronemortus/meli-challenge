from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import CustomUser, Manager, Employee, Customer


@receiver(m2m_changed, sender=CustomUser.groups.through)
def check_manager_group(sender, instance, action, **kwargs):
    if action == 'post_add' and kwargs.get('pk_set'):
        group = Group.objects.filter(pk__in=kwargs['pk_set'])
        if group.filter(name='manager').exists():
            Manager.objects.get_or_create(profile=instance)
        elif group.filter(name='employee').exists():
            Employee.objects.get_or_create(profile=instance)
        elif group.filter(name='customer').exists():
            Customer.objects.get_or_create(profile=instance)
