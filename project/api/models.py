from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timezone
from django.db.models import DateTimeField

class DateTimeWithoutTZField(DateTimeField):
    def db_type(self, connection):
        return 'timestamp'

class Bus(models.Model):
    plate = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=6)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial = models.CharField(max_length=100, unique=True)
    year = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

    @receiver(pre_save)
    def pre_save(sender, instance, **kwargs): 
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if instance._state.adding:
            instance.created_at = current_datetime
            instance.is_active = True
        else:
            instance.updated_at = current_datetime
