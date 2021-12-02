from django.db import models
from django.db.models.signals import pre_save, pre_migrate, post_migrate
from django.dispatch import receiver
from datetime import datetime, timedelta
from .helpers.date_time_without_tz_field import DateTimeWithoutTZField
import random

class Bus(models.Model):
    plate = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=6)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial = models.CharField(max_length=100, unique=True)
    year = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

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

class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

class Journey(models.Model):
    duration_in_seconds = models.PositiveBigIntegerField()
    location_origin = models.ForeignKey(Location, related_name='location_origin', on_delete=models.CASCADE)
    location_destination = models.ForeignKey(Location, related_name='location_destination', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

class Passenger(models.Model):
    document = models.CharField(max_length=15, unique=True)
    names = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    is_whitelist = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

class Seat(models.Model):

    seat_x = models.PositiveSmallIntegerField()
    seat_y = models.CharField(max_length=1)
    is_active = models.BooleanField(default=True)

    created_at = DateTimeWithoutTZField(null=True)
    updated_at = DateTimeWithoutTZField(null=True)

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

@receiver(pre_save)
def pre_save(sender, instance, **kwargs): 
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if str(type(instance)).find('Migration') == -1:
        if instance == Seat:
            instance.seat_y = instance.seat_y.upper()

        if instance == JourneyDriver:
            if instance.states:
                instance.states = 1

        if instance._state.adding:
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
            color = '000000',
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

