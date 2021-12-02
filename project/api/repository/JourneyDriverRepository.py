from django import forms
from ..models import Journey, JourneyDriver, Driver

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
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
    states = forms.IntegerField(required=False)

    journey = forms.IntegerField()
    driver = forms.IntegerField()

    def clean(self):
        data = self.cleaned_data

        if 'journey' in data:
            journey = Journey.objects.filter(id=data['journey'])
            if not journey.exists():
                self.add_error('journey', 'Does not exist')
            else:
                self.cleaned_data['journey'] = journey.first()

        if 'driver' in data:
            driver = Driver.objects.filter(id=data['driver'])
            if not driver.exists():
                self.add_error('driver', 'Does not exist')
            else:
                self.cleaned_data['driver'] = driver.first()

        if 'datetime_start' in data and self.cleaned_data['driver'] and self.cleaned_data['journey']:
            self.add_error('datetime_start', 'Required field')

        # si el journey y el driver se repiten en la tabla
        # se debe validar que no estan esos 2 id repetidos
        # en el mismo rango de tiempo
        # calculandolo a partir del "datetime_start" mas
        # el tiempo en segundos que se tarda en llegar al otro destino (duration_in_seconds de la tabla Journey)
        
        self.add_error('datetime_start', 'error de prueba')

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
    id = forms.IntegerField(required=True)
    active = forms.IntegerField(min_value=0,max_value=1,required=True)

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
        journeydriver.is_active = data['active']

        journeydriver.save()

        return modelToJson(model=journeydriver)

    def getErrors(self):
        return getErrorsFormatted(self)