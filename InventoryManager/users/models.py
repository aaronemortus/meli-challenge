from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    pass


class Manager(models.Model):
    profile = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='manager',
        limit_choices_to=Q(groups__name='manager')
    )

    def __str__(self):
        return self.profile.username


class Employee(models.Model):
    profile = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee',
        limit_choices_to=Q(groups__name='employee')
    )

    def __str__(self):
        return self.profile.username


class Customer(models.Model):
    profile = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='customer',
        limit_choices_to=Q(groups__name='customer')
    )

    def __str__(self):
        return self.profile.username
