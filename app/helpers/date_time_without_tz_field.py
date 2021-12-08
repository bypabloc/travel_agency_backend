from django.db import models

class DateTimeWithoutTZField(models.DateTimeField):
    def db_type(self, connection):
        return 'timestamp with time zone'