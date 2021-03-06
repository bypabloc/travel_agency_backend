from django import forms
from ..models import Driver, Bus, Q

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination

class DriverListForm():
    def list(self):
        params = paginate_queryset(self.request)

        drivers = Driver.objects

        drivers = model_apply_filter(model=Driver, query=drivers, params=params)
        if 'search' in params:
            drivers = drivers.filter(
                Q(document__icontains=params['search']) |
                Q(names__icontains=params['search']) |
                Q(lastname__icontains=params['search']) |
                Q(date_of_birth__icontains=params['search']) |
                Q(is_active__icontains=params['search'])
            )
            drivers = drivers.filter(
                is_active=True
            )
        drivers = model_apply_sort(model=Driver, query=drivers, params=params)
        drivers = model_apply_pagination(query=drivers, params=params)

        list = drivers['list'].all()

        list_formatted = []
        for item in list:
            list_formatted.append(modelToJson(item))

        drivers['list'] = list_formatted

        return drivers

class DriverCreateForm(forms.Form):
    document = forms.CharField(max_length=15)
    names = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    date_of_birth = forms.DateField()
    is_active = forms.BooleanField(required=False)
    bus = forms.IntegerField()
    # bus = forms.ForeignKey(Bus)

    def clean(self):
        data = self.cleaned_data

        if 'document' in data:
            if Driver.objects.filter(document=data['document']).exists():
                self.add_error('document', 'Already exists')

        if 'bus' in data:
            bus = Bus.objects.filter(id=data['bus'])
            if not bus.exists():
                self.add_error('bus', 'Does not exist')
            else:
                self.cleaned_data['bus'] = bus.first()

        return data

    def save(self):
        driver = Driver.objects.create(**self.cleaned_data)

        return modelToJson(model=driver)

    def getErrors(self):
        return getErrorsFormatted(self)

class DriverFindOneForm():
    errors = {}

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        if 'id' in params:
            self.instance = Driver.objects.filter(id=params['id'])
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

class DriverStateChangeForm(forms.Form):
    id = forms.IntegerField(required=True)
    active = forms.IntegerField(min_value=0,max_value=1,required=True)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = Driver.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()
        
        return data

    def save(self):
        data = self.cleaned_data

        driver = self.instance
        driver.is_active = data['active']

        driver.save()

        return modelToJson(model=driver)

    def getErrors(self):
        return getErrorsFormatted(self)