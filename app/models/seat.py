from ..models import models

from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Seat(models.Model):

    seat_x = models.PositiveSmallIntegerField()
    seat_y = models.CharField(max_length=1)
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)