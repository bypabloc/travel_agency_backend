from ..models import models, RawSQL, OuterRef, Subquery, RawSQL, JSONObject, JSONBAgg, ManyToManyField, apps

from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class JourneyDriverManager(models.Manager):
    def availables(self, location_origin, location_destination, date_start, date_end, tz_in_minutes=0):

        journey_driver = self.filter(
            journey__location_origin_id=location_origin,
            journey__location_destination_id=location_destination,
            # datetime_start__gte=date_start,
            # datetime_start__lte=date_end,
        ).extra(
            where = [
                '''
                    datetime_start - (%s ||\' minutes\')::interval BETWEEN %s AND %s
                ''',
            ],
            params = [
                tz_in_minutes,
                date_start,
                date_end,
            ],
        )

        journey = apps.get_model(app_label='app', model_name='Journey').objects.filter(
            journey=OuterRef('pk'),
        ).values('journey').annotate(
            list=JSONObject(
                id='id',
                duration_in_seconds='duration_in_seconds',
                is_active='is_active',
                created_at='created_at',
                updated_at='updated_at',
            ),
        ).values('list')
        journey_driver = journey_driver.annotate(
            journey_data=Subquery(journey),
        )

        driver = apps.get_model(app_label='app', model_name='Driver').objects.filter(
            driver=OuterRef('pk'),
        ).values('driver').annotate(
            list=JSONObject(
                id='id',
                document='document',
                names='names',
                lastname='lastname',
                date_of_birth='date_of_birth',
                is_active='is_active',
                created_at='created_at',
                updated_at='updated_at',
            ),
        ).values('list')
        journey_driver = journey_driver.annotate(
            driver_data=Subquery(driver),
        )

        tickets_subquery = apps.get_model(app_label='app', model_name='Ticket').objects.filter(
            journey_driver=OuterRef('pk'),
        ).values('id').annotate(
            list=JSONBAgg(
                JSONObject(
                    created_at='created_at',
                    updated_at='updated_at',
                ),
            ),
        ).values('list')
        journey_driver = journey_driver.annotate(
            tickets_data=Subquery(tickets_subquery),
        )
        print('journey_driver.query', journey_driver.query)

        journey_driver = journey_driver.annotate(
            seats=RawSQL(
                """
                    SELECT 
                        JSONB_AGG(
                            JSONB_BUILD_OBJECT(
                                'available', (
                                    SELECT
                                        CASE
                                            WHEN COUNT(*) > 0 THEN false
                                            ELSE true
                                        END
                                    FROM "app_ticket" ticket
                                    WHERE ticket.seat_id = seat."id" AND ticket.journey_driver_id = app_journeydriver.id
                                ), 
                                'id', seat."id", 
                                'x', seat."seat_x", 
                                'y', seat."seat_y"
                            ) 
                        ) AS "list" 
                    FROM "app_seat" seat 
                    WHERE seat."is_active" = true
	
                """,
                ()
            ),
        )

        return journey_driver
        
    def fields_custom(self, bus=None, average_capacity_sold=None, journey=None):
        
        journey_driver = self 

        if bus:
            journey_driver = journey_driver.filter(
                driver__bus_id=bus,
            )

        if journey:
            journey_driver = journey_driver.filter(
                journey_id=journey,
            )

        if average_capacity_sold:
            journey_driver = journey_driver.filter(
                states=RawSQL(
                    """
                        (
                            CASE
                                WHEN (
                                    (
                                        (
                                            (
                                                SELECT 
                                                    COUNT(*)
                                                FROM 
                                                    app_ticket AS ticket
                                                WHERE 
                                                    ticket.journey_driver_id = app_journeydriver.id
                                                GROUP BY ticket.journey_driver_id
                                            )::NUMERIC(10,2)
                                            /
                                            (
                                                SELECT
                                                    COUNT(*)
                                                FROM "app_seat" seat
                                                WHERE seat."is_active" = true
                                            )::NUMERIC(10,2)
                                        )::NUMERIC(10,2)
                                        * 100
                                    )::NUMERIC(10,2)
                                ) >= %s THEN 1
                                ELSE 0
                            END
                        )
                    """,
                    (average_capacity_sold,)
                ),
            )
        
        journey = apps.get_model(app_label='app', model_name='Journey').objects.filter(
            journey=OuterRef('pk'),
        ).values('journey').annotate(
            list=JSONObject(
                id='id',
                location_origin=RawSQL(
                    """
                    (
                        SELECT
                            JSONB_BUILD_OBJECT(
                                'id', location."id",
                                'name', location."name",
                                'created_at', location."created_at",
                                'updated_at', location."updated_at"
                            )
                        FROM "app_location" location
                        WHERE location."id" = u0.location_origin_id
                    )
                    """,
                    ()
                ),
                location_destination=RawSQL(
                    """
                    (
                        SELECT
                            JSONB_BUILD_OBJECT(
                                'id', location."id",
                                'name', location."name",
                                'created_at', location."created_at",
                                'updated_at', location."updated_at"
                            )
                        FROM "app_location" location
                        WHERE location."id" = u0.location_destination_id
                    )
                    """,
                    ()
                ),
                duration_in_seconds='duration_in_seconds',
                is_active='is_active',
                created_at='created_at',
                updated_at='updated_at',
            ),
        ).values('list')
        journey_driver = journey_driver.annotate(
            journey_data=Subquery(journey),
        )
        print('journey_driver.query', journey_driver.query)

        driver = apps.get_model(app_label='app', model_name='Driver').objects.filter(
            driver=OuterRef('pk'),
        ).values('driver').annotate(
            list=JSONObject(
                id='id',
                document='document',
                names='names',
                lastname='lastname',
                date_of_birth='date_of_birth',
                bus=RawSQL(
                    """
                    (
                        SELECT
                            JSONB_BUILD_OBJECT(
                                'id', bus."id",
                                'plate', bus."plate",
                                'brand', bus."brand",
                                'model', bus."model",
                                'year', bus."year",
                                'is_active', bus."is_active",
                                'created_at', bus."created_at",
                                'updated_at', bus."updated_at"
                            )
                        FROM "app_bus" bus
                        WHERE bus."id" = u0.bus_id
                    )
                    """,
                    ()
                ),
                is_active='is_active',
                created_at='created_at',
                updated_at='updated_at',
            ),
        ).values('list')
        journey_driver = journey_driver.annotate(
            driver_data=Subquery(driver),
        )

        tickets_subquery = apps.get_model(app_label='app', model_name='Ticket').objects.filter(
            journey_driver=OuterRef('pk'),
        ).values('id').annotate(
            list=JSONBAgg(
                JSONObject(
                    created_at='created_at',
                    updated_at='updated_at',
                ),
            ),
        ).values('list')
        journey_driver = journey_driver.annotate(
            tickets_data=Subquery(tickets_subquery),
        )

        journey_driver = journey_driver.annotate(
            seats=RawSQL(
                """
                    SELECT 
                        JSONB_AGG(
                            JSONB_BUILD_OBJECT(
                                'available', (
                                    SELECT
                                        CASE
                                            WHEN COUNT(*) > 0 THEN false
                                            ELSE true
                                        END
                                    FROM "app_ticket" ticket
                                    WHERE ticket.seat_id = seat."id" AND ticket.journey_driver_id = app_journeydriver.id
                                ), 
                                'id', seat."id", 
                                'x', seat."seat_x", 
                                'y', seat."seat_y"
                            ) 
                        ) AS "list" 
                    FROM "app_seat" seat 
                    WHERE seat."is_active" = true
	
                """,
                ()
            ),
        )

        journey_driver = journey_driver.annotate(
            average_capacity_sold=RawSQL(
                """
                    (
                        (
                            (
                                SELECT 
                                    COUNT(*)
                                FROM 
                                    app_ticket AS ticket
                                WHERE 
                                    ticket.journey_driver_id = app_journeydriver.id
                                GROUP BY ticket.journey_driver_id
                            )::NUMERIC(10,2)
                            /
                            (
                                SELECT
                                    COUNT(*)
                                FROM "app_seat" seat
                                WHERE seat."is_active" = true
                            )::NUMERIC(10,2)
                        )::NUMERIC(10,2)
                        * 100
                    )::NUMERIC(10,2)
                """,
                ()
            ),
        )

        return journey_driver
        
class JourneyDriver(models.Model):
    datetime_start = DateTimeWithoutTZField(null=True)
    states = models.PositiveSmallIntegerField()

    journey = models.ForeignKey(
        'Journey',
        related_name='journey',
        on_delete=models.CASCADE, 
    )
    driver = models.ForeignKey(
        'Driver', 
        related_name='driver', 
        on_delete=models.CASCADE, 
    )

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

    objects = JourneyDriverManager()
