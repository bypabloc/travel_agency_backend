from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Bus(models.Model):
    plate = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=6)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial = models.CharField(max_length=100, unique=True)
    year = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)

    @receiver(pre_save)
    def pre_save(sender, instance, **kwargs): 
        if instance._state.adding:
            instance.is_active = True
        else:
            instance.updated_at = now()
