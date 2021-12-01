from django.db import models
from django.utils.timezone import now

class Bus(models.Model):
    plate = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=6)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial = models.CharField(max_length=100, unique=True)
    year = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)

    # class Meta:
        # managed = False
        # db_table = "uasdser"

    def __str__(self):
        return self.name