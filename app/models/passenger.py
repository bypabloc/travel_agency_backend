from ..models import models

from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Passenger(models.Model):
    document = models.CharField(max_length=15, unique=True)
    names = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    is_whitelist = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)