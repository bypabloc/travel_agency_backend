from django import forms
from ..models import Bus

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination

from datetime import date

class BusListForm():
    def list(self):
        request = self.request

        params = paginate_queryset(request)

        buses = Bus.objects

        buses = model_apply_filter(model=Bus, query=buses, params=params)
        buses = model_apply_sort(model=Bus, query=buses, params=params)

        return model_apply_pagination(query=buses, params=params)

class BusCreateForm(forms.Form):
    plate = forms.CharField(max_length=10)
    color = forms.CharField(max_length=6)
    brand = forms.CharField(max_length=50)
    model = forms.CharField(max_length=50)
    serial = forms.CharField(max_length=100)
    year = forms.IntegerField(min_value=1000,max_value=date.today().year)
    is_active = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data

        if 'plate' in data:
            if Bus.objects.filter(plate=data['plate']).exists():
                self.add_error('plate', 'Already exists')

        if 'serial' in data:
            if Bus.objects.filter(serial=data['serial']).exists():
                self.add_error('serial', 'Already exists')
        
        return data

    def save(self):
        bus = Bus.objects.create(**self.cleaned_data)
        return modelToJson(model=bus)

    def getErrors(self):
        return getErrorsFormatted(self)

class BusFindOneForm():
    errors = {}

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        if 'id' in params:
            self.instance = Bus.objects.filter(id=params['id'])
            if not self.instance.exists():
                self.add_error(field='id', error='Not exists')
        else:
            self.add_error('id', 'Field is required')

        return False if len(self.errors) > 0 else True

    def find(self):
        return self.instance.all().values().first()

    def add_error(self, field, error):
        if field in self.errors:
            self.errors[field].append(error)
        else:
            self.errors[field] = [error]

    def getErrors(self):
        return self.errors

class BusStateChangeForm(forms.Form):
    id = forms.IntegerField(required=True)
    active = forms.IntegerField(min_value=0,max_value=1,required=True)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = Bus.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()
        
        return data

    def save(self):
        data = self.cleaned_data

        bus = self.instance
        bus.is_active = data['active']

        bus.save()

        return modelToJson(model=bus)

    def getErrors(self):
        return getErrorsFormatted(self)