from ..models import models, RawSQL, OuterRef, Subquery, JSONObject, JSONBAgg

from .location import Location
from .journey_driver import JourneyDriver

from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class JourneyManager(models.Manager):
    def average_passengers(self):

        location_origin = Location.objects.filter(
            location_origin=OuterRef('pk'),
        ).values('location_origin').annotate(
            list=JSONObject(
                id='id',
                name='name',
                is_active='is_active',
                created_at='created_at',
                updated_at='updated_at',
            ),
        ).values('list')

        location_destination = Location.objects.filter(
            location_destination=OuterRef('pk'),
        ).values('location_destination').annotate(
            list=JSONObject(
                id='id',
                name='name',
                is_active='is_active',
                created_at='created_at',
                updated_at='updated_at',
            ),
        ).values('list')

        return self.annotate(
            quantity_ticket_sold=RawSQL(
                """
                    (
                        SELECT 
                            COUNT(*)
                        FROM 
                            app_journeydriver AS jd
                        RIGHT JOIN app_ticket AS ticket ON ticket.journey_driver_id = jd.id
                        WHERE 
                            jd.journey_id = app_journey.id 
                        GROUP BY jd.journey_id
                    )::NUMERIC(10,2)
                """,
                ()
            ),
            quantity_journey_driver=RawSQL(
                """
                    (
                        SELECT 
                            COUNT(*)
                        FROM 
                            app_journeydriver AS jd
                        WHERE 
                            jd.journey_id = app_journey.id 
                        GROUP BY jd.journey_id
                    )::NUMERIC(10,2)
                """,
                ()
            ),
            average_passengers=RawSQL(
                """
                    (
                        (
                            (
                                SELECT 
                                    COUNT(*)
                                FROM 
                                    app_journeydriver AS jd
                                RIGHT JOIN app_ticket AS ticket ON ticket.journey_driver_id = jd.id
                                WHERE 
                                    jd.journey_id = app_journey.id 
                                GROUP BY jd.journey_id
                            )::NUMERIC(10,2)
                        )
                        /
                        (
                            (
                                SELECT 
                                    COUNT(*)
                                FROM 
                                    app_journeydriver AS jd
                                WHERE 
                                    jd.journey_id = app_journey.id 
                                GROUP BY jd.journey_id
                            )::NUMERIC(10,2)
                        )
                    )::NUMERIC(10,2)
                """,
                ()
            ),
            location_origin_data=Subquery(location_origin),
            location_destination_data=Subquery(location_destination),
        )

    def journeys_drivers(self):

        journeys_drivers = JourneyDriver.objects.tickets().filter(
            journey_id=OuterRef('pk'),
        ).values('journey_id').annotate(
            list=JSONBAgg(
                JSONObject(
                    datetime_start='datetime_start',
                    states='states',
                    journey='journey',
                    driver='driver',
                    created_at='created_at',
                    updated_at='updated_at',
                ),
            ),
        ).values('list')

        return self.annotate(
            journeys_drivers=Subquery(journeys_drivers),
        )

class Journey(models.Model):
    duration_in_seconds = models.PositiveBigIntegerField()
    location_origin = models.ForeignKey(Location, related_name='location_origin', on_delete=models.CASCADE)
    location_destination = models.ForeignKey(Location, related_name='location_destination', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

    objects = JourneyManager()