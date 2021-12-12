from ..models import models, RawSQL, RawSQL

from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class BusManager(models.Manager):
    def filters_custom(self, **kwargs):

        buses = self

        if 'more_than_percentage_of_capacity_sold' in kwargs:
            more_than_percentage_of_capacity_sold = kwargs['more_than_percentage_of_capacity_sold']

            buses = buses.extra(
                where = [
                    '''
                    (
                        SELECT
                            COUNT(*)
                        FROM
                            "app_driver"
                        INNER JOIN "app_journeydriver" ON "app_journeydriver"."driver_id" = "app_driver"."id"
                        INNER JOIN "app_ticket" ON "app_ticket"."journey_driver_id" = "app_journeydriver"."id"
                        WHERE
                            "app_driver"."bus_id" = "app_bus"."id"
                        GROUP BY
                            "app_driver"."bus_id"
                    )
                    / 
                    (
                        SELECT
                            COUNT(*)
                        FROM "app_seat" seat
                        WHERE seat."is_active" = true
                    )
                    > %s
                    ''',
                ],
                params = [
                    more_than_percentage_of_capacity_sold,
                ],
            ).annotate(
                percentage_of_capacity_sold=RawSQL(
                    """
                        (
                            SELECT
                                COUNT(*)
                            FROM
                                "app_driver"
                            INNER JOIN "app_journeydriver" ON "app_journeydriver"."driver_id" = "app_driver"."id"
                            INNER JOIN "app_ticket" ON "app_ticket"."journey_driver_id" = "app_journeydriver"."id"
                            WHERE
                                "app_driver"."bus_id" = "app_bus"."id"
                            GROUP BY
                                "app_driver"."bus_id"
                        )
                        /
                        (
                            SELECT
                                COUNT(*)
                            FROM "app_seat" seat
                            WHERE seat."is_active" = true
                        )
                    """,
                    ()
                )
            )

        if 'journey' in kwargs:
            journey = kwargs['journey']

            buses = buses.extra(
                where = [
                    '''
                        SELECT
                            CASE 
                                WHEN COUNT(*) > 0 THEN TRUE
                                ELSE FALSE
                            END
                        FROM 
                            "app_driver"
                        INNER JOIN "app_journeydriver" ON "app_journeydriver"."driver_id" = "app_driver"."id"
                        WHERE
                            "app_driver"."bus_id" = "app_bus"."id"
                            AND "app_journeydriver"."journey_id" = %s
                        LIMIT 1
                    ''',
                ],
                params = [
                    journey,
                ],
            )

        return buses

class Bus(models.Model):
    plate = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=7)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial = models.CharField(max_length=100, unique=True)
    year = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    objects = BusManager()

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)
