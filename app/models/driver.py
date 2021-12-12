from ..models import models

from .bus import Bus

from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Driver(models.Model):
    document = models.CharField(max_length=15, unique=True)
    names = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    bus = models.ForeignKey(Bus, related_name='bus', on_delete=models.CASCADE)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)
