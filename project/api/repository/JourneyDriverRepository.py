from django import forms
from datetime import datetime, timedelta

from ..models import Journey, JourneyDriver, Driver

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
from ..helpers.request_get_tz import get_request_tz
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination

class JourneyDriverListForm():
    def list(self):
        params = paginate_queryset(self.request)

        journeysdrivers = JourneyDriver.objects

        journeysdrivers = model_apply_filter(model=JourneyDriver, query=journeysdrivers, params=params)
        journeysdrivers = model_apply_sort(model=JourneyDriver, query=journeysdrivers, params=params)
        journeysdrivers = model_apply_pagination(query=journeysdrivers, params=params)

        list = journeysdrivers['list'].all()

        list_formatted = []
        for item in list:
            list_formatted.append(modelToJson(item))

        journeysdrivers['list'] = list_formatted

        return journeysdrivers

class JourneyDriverCreateForm(forms.Form):
    datetime_start = forms.DateTimeField()
    states = forms.IntegerField(required=False,min_value=1, max_value=5)

    journey = forms.IntegerField()
    driver = forms.IntegerField()

    def clean(self):
        data = self.cleaned_data

        journey = False
        if 'journey' in data:
            journey = Journey.objects.filter(id=data['journey'])
            if not journey.exists():
                self.add_error('journey', 'Does not exist')
            else:
                journey = journey.first()
                self.cleaned_data['journey'] = journey

        driver = False
        if 'driver' in data:
            driver = Driver.objects.filter(id=data['driver'])
            if not driver.exists():
                self.add_error('driver', 'Does not exist')
            else:
                driver = driver.first()
                self.cleaned_data['driver'] = driver

        if 'datetime_start' in data and driver and journey:
            datetime_start = data['datetime_start']

            tz_in_minutes = get_request_tz(self.request)

            journey_duration_in_minutes = journey.duration_in_seconds/60

            datetime_start_with_tz = datetime_start + timedelta(minutes=tz_in_minutes)

            if datetime.now() > datetime_start_with_tz:
                self.add_error('datetime_start', 'Cannot be in the past')
            else:
                journeys_drivers = JourneyDriver.objects.filter(
                    journey=journey.id,
                    driver=driver.id,
                ).extra(
                    where=['%s BETWEEN datetime_start AND datetime_start + (%s ||\' minutes\')::interval'],
                    params=[datetime_start_with_tz, journey_duration_in_minutes],
                )
                if journeys_drivers.exists():
                    journey_driver = journeys_drivers.last()
                    datetime_start_suggested = (journey_driver.datetime_start + timedelta(minutes=journey_duration_in_minutes) - timedelta(minutes=tz_in_minutes) ) 

                    self.add_error('datetime_start', 'There is already a journey and an assigned driver for this schedule, please choose another time')
                    self.add_error('datetime_start', 'NOTE: the next suggested date is: '+ datetime_start_suggested.strftime('%Y-%m-%d %H:%M:%S'))

                else:
                    self.cleaned_data['datetime_start'] = datetime_start_with_tz

        return data

    def save(self):
        journeydriver = JourneyDriver.objects.create(**self.cleaned_data)
        return modelToJson(model=journeydriver)

    def getErrors(self):
        return getErrorsFormatted(self)

class JourneyDriverFindOneForm():
    errors = {}

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        if 'id' in params:
            self.instance = JourneyDriver.objects.filter(id=params['id'])
            if not self.instance.exists():
                self.add_error(field='id', error='Not exists')
        else:
            self.add_error('id', 'Field is required')

        return False if len(self.errors) > 0 else True

    def find(self):
        return modelToJson(model=self.instance.all().first())

    def add_error(self, field, error):
        if field in self.errors:
            self.errors[field].append(error)
        else:
            self.errors[field] = [error]

    def getErrors(self):
        return self.errors

class JourneyDriverStateChangeForm(forms.Form):
    id = forms.IntegerField()
    states = forms.IntegerField(min_value=1, max_value=5)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = JourneyDriver.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()
        
        return data

    def save(self):
        data = self.cleaned_data

        journeydriver = self.instance
        journeydriver.states = data['states']

        journeydriver.save()

        return modelToJson(model=journeydriver)

    def getErrors(self):
        return getErrorsFormatted(self)

class JourneyDriverChangeDriverForm(forms.Form):
    id = forms.IntegerField()
    driver = forms.IntegerField()

    def clean(self):
        data = self.cleaned_data

        self.instance = False
        if 'id' in data:
            self.instance = JourneyDriver.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()

        driver = False
        if 'driver' in data:
            if self.instance and data['driver'] == self.instance.driver.id:
                self.add_error('driver', 'It must indicate a different driver')
            else:
                driver = Driver.objects.filter(id=data['driver'])
                if not driver.exists():
                    self.add_error('driver', 'Does not exist')
                else:
                    driver = driver.first()
                    self.cleaned_data['driver'] = driver

        if self.instance and driver:

            journey_driver = self.instance
            journey_duration_in_minutes = journey_driver.journey.duration_in_seconds/60
            datetime_start_with_tz = journey_driver.datetime_start

            journeys_drivers = JourneyDriver.objects.filter(
                driver=driver.id,
            ).extra(
                where=['%s BETWEEN datetime_start AND datetime_start + (%s ||\' minutes\')::interval'],
                params=[datetime_start_with_tz, journey_duration_in_minutes],
            )
            if journeys_drivers.exists():
                self.add_error('driver', 'You cannot assign this driver to this schedule, as it is assigned to another schedule on another journey.')

        return data

    def save(self):
        data = self.cleaned_data

        journeydriver = self.instance
        journeydriver.driver = data['driver']

        journeydriver.save()

        return modelToJson(model=journeydriver)

    def getErrors(self):
        return getErrorsFormatted(self)
