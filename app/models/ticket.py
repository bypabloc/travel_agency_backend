from ..models import models

from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Ticket(models.Model):
    states = models.PositiveSmallIntegerField()

    passenger = models.ForeignKey(
        'Passenger', 
        related_name='passenger', 
        on_delete=models.CASCADE, 
    )
    journey_driver = models.ForeignKey(
        'JourneyDriver', 
        related_name='journey_driver', 
        on_delete=models.CASCADE, 
    )
    seat = models.ForeignKey(
        'Seat', 
        related_name='seat', 
        on_delete=models.CASCADE, 
    )

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)