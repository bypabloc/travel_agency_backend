from ..models import models, RawSQL

from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class LocationManager(models.Manager):
    def available(self):
        return self.filter(is_active__gte=RawSQL('''
                    (
                        SELECT
                            COUNT(*) AS "is_active"
                        FROM
                            "app_journey"
                        INNER JOIN "app_journeydriver" ON "app_journeydriver"."journey_id" = "app_journey"."id"
                        WHERE
                            (
                                "app_journey"."location_origin_id" = "app_location"."id" OR "app_journey"."location_destination_id" = "app_location"."id"
                            )
                            AND "app_journeydriver"."states" = 1
                        GROUP BY
                            "app_location"."id"
                    ) > %s
                    ''', (0,)))

class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

    objects = LocationManager()
