from django import forms
from ..models import Bus
from .helpers import getErrorsFormatted

class BusCreateForm(forms.Form):
    plate = forms.CharField(max_length=10, required=True)
    color = forms.CharField(max_length=6)
    brand = forms.CharField(max_length=50)
    model = forms.CharField(max_length=50)
    serial = forms.CharField(max_length=100, required=True)
    year = forms.DateField()
    is_active = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data

        print('BusCreateForm -> clean: ', data)

        if 'plate' in data:
            if Bus.objects.filter(plate=data['plate']).exists():
                self.add_error('plate', 'Already exists')

        if 'serial' in data:
            if Bus.objects.filter(serial=data['serial']).exists():
                self.add_error('serial', 'Already exists')
        
        return data

    def save(self):
        return Bus.objects.create(**self.cleaned_data)

    def getErrors(self):
        return getErrorsFormatted(self)

class BusFindOneForm(forms.Form):
    id = forms.IntegerField(required=True)

    def clean(self):
        data = self.cleaned_data

        print('BusFindOneForm -> clean: ', data)

        if 'id' in data:
            if not Bus.objects.filter(id=data['id']).exists():
                self.add_error('id', 'Not exists')
        
        return data

    def find(self):
        return Bus.objects.filter(**self.cleaned_data).all().values().first()

    def getErrors(self):
        return getErrorsFormatted(self)

class BusStateChangeForm(forms.Form):
    id = forms.IntegerField(required=True)
    active = forms.IntegerField(min_value=0,max_value=1,required=True)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            if not Bus.objects.filter(id=data['id']).exists():
                self.add_error('id', 'Not exists')
        
        return data

    def save(self):
        data = self.cleaned_data

        bus = Bus.objects.get(id=data['id'])
        bus.is_active = data['active']
        bus.save()

        return bus

    def getErrors(self):
        return getErrorsFormatted(self)