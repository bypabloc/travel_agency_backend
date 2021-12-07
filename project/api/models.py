from django.db import models
from django.db.models.expressions import OuterRef, Subquery, RawSQL
from django.db.models.functions import JSONObject
from django.contrib.postgres.aggregates.general import JSONBAgg

from django.db.models.signals import pre_save, pre_migrate, post_migrate
from django.dispatch import receiver
from datetime import datetime, timedelta

from .helpers.date_time_without_tz_field import DateTimeWithoutTZField
import random

Q = models.Q
Exists = models.Exists
OuterRef = OuterRef

class BusManager(models.Manager):
    def filters_custom(self, **kwargs):

        print('kwargs: ', kwargs)

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
                            "api_driver"
                        INNER JOIN "api_journeydriver" ON "api_journeydriver"."driver_id" = "api_driver"."id"
                        INNER JOIN "api_ticket" ON "api_ticket"."journey_driver_id" = "api_journeydriver"."id"
                        WHERE
                            "api_driver"."bus_id" = "api_bus"."id"
                        GROUP BY
                            "api_driver"."bus_id"
                    ) / 10 > %s
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
                                "api_driver"
                            INNER JOIN "api_journeydriver" ON "api_journeydriver"."driver_id" = "api_driver"."id"
                            INNER JOIN "api_ticket" ON "api_ticket"."journey_driver_id" = "api_journeydriver"."id"
                            WHERE
                                "api_driver"."bus_id" = "api_bus"."id"
                            GROUP BY
                                "api_driver"."bus_id"
                        ) / 10
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
                            "api_driver"
                        INNER JOIN "api_journeydriver" ON "api_journeydriver"."driver_id" = "api_driver"."id"
                        WHERE
                            "api_driver"."bus_id" = "api_bus"."id"
                            AND "api_journeydriver"."journey_id" = %s
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

class Driver(models.Model):
    document = models.CharField(max_length=15, unique=True)
    names = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    bus = models.ForeignKey(Bus, related_name='bus', on_delete=models.CASCADE)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

class LocationManager(models.Manager):
    def available(self):
        return self.filter(is_active__gte=RawSQL('''
                    (
                        SELECT
                            COUNT(*) AS "is_active"
                        FROM
                            "api_journey"
                        INNER JOIN "api_journeydriver" ON "api_journeydriver"."journey_id" = "api_journey"."id"
                        WHERE
                            (
                                "api_journey"."location_origin_id" = "api_location"."id" OR "api_journey"."location_destination_id" = "api_location"."id"
                            )
                            AND "api_journeydriver"."states" = 1
                        GROUP BY
                            "api_location"."id"
                    ) > %s
                    ''', (0,)))
        return self.aggregation(
                where = [
                    '''
                    (
                        SELECT
                            COUNT(*)
                        FROM
                            "api_journey"
                        INNER JOIN "api_journeydriver" ON "api_journeydriver"."journey_id" = "api_journey"."id"
                        WHERE
                            (
                                "api_journey"."location_origin_id" = "api_location"."id" OR "api_journey"."location_destination_id" = "api_location"."id"
                            )
                            AND "api_journeydriver"."states" = 1
                        GROUP BY
                            "api_location"."id"
                    ) > 0
                    ''',
                ],
            )

class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

    objects = LocationManager()


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

        # # Query para un listado
        # location_origin = Location.objects.filter(
        #     location_origin=OuterRef('pk'),
        # ).values('location_origin').annotate(
        #     list=JSONBAgg(
        #         JSONObject(
        #             created_at='created_at',
        #             updated_at='updated_at',
        #         ),
        #     ),
        # ).values('list')

        return self.annotate(
            average_passengers=RawSQL(
                """
                    SELECT 
                        AVG (1)::NUMERIC(10,2)
                    FROM 
                        api_journeydriver AS jd
                    RIGHT JOIN api_ticket AS ticket ON ticket.journey_driver_id = jd.id
                    WHERE 
                        jd.journey_id = api_journey.id  
                    GROUP BY jd.id
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

class Passenger(models.Model):
    document = models.CharField(max_length=15, unique=True)
    names = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    is_whitelist = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

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

        journey = Journey.objects.filter(
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

        driver = Driver.objects.filter(
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

        tickets_subquery = Ticket.objects.filter(
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
                                    FROM "api_ticket" ticket
                                    WHERE ticket.seat_id = seat."id" AND ticket.journey_driver_id = api_journeydriver.id
                                ), 
                                'id', seat."id", 
                                'seat_x', seat."seat_x", 
                                'seat_y', seat."seat_y"
                            ) 
                        ) AS "list" 
                    FROM "api_seat" seat 
                    WHERE seat."is_active" = true
	
                """,
                ()
            ),
        )

        return journey_driver
        

class JourneyDriver(models.Model):
    datetime_start = DateTimeWithoutTZField(null=True)
    states = models.PositiveSmallIntegerField()

    journey = models.ForeignKey(
        Journey, 
        related_name='journey', 
        on_delete=models.CASCADE, 
    )
    driver = models.ForeignKey(
        Driver, 
        related_name='driver', 
        on_delete=models.CASCADE, 
    )

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

    objects = JourneyDriverManager()

class Seat(models.Model):

    seat_x = models.PositiveSmallIntegerField()
    seat_y = models.CharField(max_length=1)
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

class Ticket(models.Model):
    states = models.PositiveSmallIntegerField()

    passenger = models.ForeignKey(
        Passenger, 
        related_name='passenger', 
        on_delete=models.CASCADE, 
    )
    journey_driver = models.ForeignKey(
        JourneyDriver, 
        related_name='journey_driver', 
        on_delete=models.CASCADE, 
    )
    seat = models.ForeignKey(
        Seat, 
        related_name='seat', 
        on_delete=models.CASCADE, 
    )

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

@receiver(pre_save)
def pre_save(sender, instance, **kwargs): 
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    name_instance = str(type(instance))
    if name_instance.find('Migration') == -1:

        if instance._state.adding:

            if name_instance.find('Seat') != -1:
                instance.seat_y = instance.seat_y.upper()
            elif name_instance.find('JourneyDriver') != -1:
                if not instance.states:
                    instance.states = 1
            elif name_instance.find('Ticket') != -1:
                if not instance.states:
                    instance.states = 1

            instance.created_at = current_datetime
            instance.is_active = True
        else:
            instance.updated_at = current_datetime

@receiver(pre_migrate)
def pre_migrate(sender, **kwargs):
    print('\n\n')
    print('pre_migrate')
    print('\n\n')

    try:
        Bus.objects.all().delete()
        Driver.objects.all().delete()
        Location.objects.all().delete()
        Journey.objects.all().delete()
        Passenger.objects.all().delete()
        Seat.objects.all().delete()
        JourneyDriver.objects.all().delete()
    except Exception as e:
        pass

@receiver(post_migrate)
def post_migrate(sender, plan, **kwargs):
    print('post_migrate')

    try:
        Bus.objects.create(
            plate = 'X-123',
            color = '#000000',
            brand = 'Toyota',
            model = 'Corolla',
            serial = '123456789',
            year = '2021',
            is_active = True,
        )
    except Exception as e:
        print('Bus -> Exception ',e)
        pass

    try:
        buses_random = random_objects(model=Bus.objects)

        Driver.objects.create(
            document = '123456789',
            names = 'Juan',
            lastname = 'Perez',
            date_of_birth = '2000-01-01',
            is_active = True,
            bus = buses_random['one'],
        )
    except Exception as e:
        print('Driver -> Exception ',e)
        pass

    try:
        Location.objects.create(
            name = 'Cali',
            is_active = True,
        )
        Location.objects.create(
            name = 'Bogota',
            is_active = True,
        )
        Location.objects.create(
            name = 'Medellin',
            is_active = True,
        )
        Location.objects.create(
            name = 'Cartagena',
            is_active = True,
        )
        Location.objects.create(
            name = 'Barranquilla',
            is_active = True,
        )
        Location.objects.create(
            name = 'Cucuta',
            is_active = True,
        )
        Location.objects.create(
            name = 'Bucaramanga',
            is_active = True,
        )
        Location.objects.create(
            name = 'Manizales',
            is_active = True,
        )
        Location.objects.create(
            name = 'Villavicencio',
            is_active = True,
        )
        Location.objects.create(
            name = 'Pasto',
            is_active = True,
        )
        Location.objects.create(
            name = 'Monteria',
            is_active = True,
        )
        Location.objects.create(
            name = 'Neiva',
            is_active = True,
        )
        Location.objects.create(
            name = 'Armenia',
            is_active = True,
        )
        Location.objects.create(
            name = 'Pereira',
            is_active = True,
        )

    except Exception as e:
        print('Location -> Exception ',e)
        pass

    try:
        locations_random = random_objects(model=Location.objects)

        Journey.objects.create(
            duration_in_seconds = random.randint(3600, (3600*24)),
            location_origin = locations_random['many'][0],
            location_destination = locations_random['many'][1],
            is_active = True,
        )
    except Exception as e:
        print('Journey -> Exception ',e)
        pass

    try:
        Seat.objects.create(
            seat_x=1,
            seat_y='A'
        )
        Seat.objects.create(
            seat_x=1,
            seat_y='B'
        )
        Seat.objects.create(
            seat_x=2,
            seat_y='B'
        )
        Seat.objects.create(
            seat_x=3,
            seat_y='B'
        )
        Seat.objects.create(
            seat_x=1,
            seat_y='C'
        )
        Seat.objects.create(
            seat_x=2,
            seat_y='C'
        )
        Seat.objects.create(
            seat_x=3,
            seat_y='C'
        )
        Seat.objects.create(
            seat_x=1,
            seat_y='D'
        )
        Seat.objects.create(
            seat_x=2,
            seat_y='D'
        )
        Seat.objects.create(
            seat_x=3,
            seat_y='D'
        )
    except Exception as e:
        print('Seat -> Exception ',e)
        pass

    try:
        Passenger.objects.create(
            document = '123456789',
            names = 'Carlos',
            lastname = 'Acosta',
            date_of_birth = '2002-01-01',
            is_whitelist = True,
        )
        Passenger.objects.create(
            document = '223456789',
            names = 'Luis',
            lastname = 'Mendoza',
            date_of_birth = '2005-01-01',
            is_whitelist = True,
        )
    except Exception as e:
        print('Passenger -> Exception ',e)
        pass

    try:
        journey = random_objects(model=Journey.objects)
        driver = random_objects(model=Driver.objects)

        JourneyDriver.objects.create(
            datetime_start = gen_datetime(),
            journey = journey['one'],
            driver = driver['one'],
            states = random.randint(1,5),
        )

        JourneyDriver.objects.create(
            datetime_start = gen_datetime(),
            journey = journey['one'],
            driver = driver['one'],
            states = random.randint(1,5),
        )

        JourneyDriver.objects.create(
            datetime_start = gen_datetime(),
            journey = journey['one'],
            driver = driver['one'],
            states = random.randint(1,5),
        )
        
    except Exception as e:
        print('JourneyDriver -> Exception ',e)
        pass

def random_objects(model):
    items = list(model.all())
    return {
        'one': random.choice(items),
        'many': random.sample(items, model.count()),
    }

def gen_datetime(max_year=datetime.now().year+1):
    start = datetime.now()
    years = max_year - start.year
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

