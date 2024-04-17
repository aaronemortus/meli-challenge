from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Sale


@receiver(post_save, sender=Sale)
def update_sale_status(sender, instance, created, **kwargs):
    if created:
        instance.status = Sale.SOLD
        instance.save()