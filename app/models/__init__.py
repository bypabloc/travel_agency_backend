from django.db import models
from django.db.models import Q, ManyToManyField, ForeignKey
from django.apps import apps
from django.db.models import Exists
from django.db.models.expressions import OuterRef, Subquery, RawSQL
from django.db.models.functions import JSONObject
from django.contrib.postgres.aggregates.general import JSONBAgg

from django.db.models.signals import pre_save, pre_migrate, post_migrate
from django.dispatch import receiver
import random
from datetime import datetime, timedelta

from .bus import Bus
from .driver import Driver
from .location import Location
from .journey import Journey
from .journey_driver import JourneyDriver
from .passenger import Passenger
from .seat import Seat
from .ticket import Ticket

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
    pass

@receiver(post_migrate)
def post_migrate(sender, plan, **kwargs):
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

