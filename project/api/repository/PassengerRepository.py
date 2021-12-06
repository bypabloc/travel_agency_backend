from django import forms
from ..models import Passenger, Q

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination

class PassengerListForm():
    def list(self):
        params = paginate_queryset(self.request)

        passengers = Passenger.objects

        passengers = model_apply_filter(model=Passenger, query=passengers, params=params)
        if 'search' in params:
            passengers = passengers.filter(
                Q(document__icontains=params['search']) |
                Q(names__icontains=params['search']) |
                Q(lastname__icontains=params['search']) |
                Q(date_of_birth__icontains=params['search'])
            )
            passengers = passengers.filter(
                is_whitelist=True
            )
        passengers = model_apply_sort(model=Passenger, query=passengers, params=params)
        passengers = model_apply_pagination(query=passengers, params=params)

        list = passengers['list'].all()

        list_formatted = []
        for item in list:
            list_formatted.append(modelToJson(item))

        passengers['list'] = list_formatted

        return passengers

class PassengerCreateForm(forms.Form):
    document = forms.CharField(max_length=15)
    names = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    date_of_birth = forms.DateField()
    is_whitelist = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data

        if 'document' in data:
            if Passenger.objects.filter(document=data['document']).exists():
                self.add_error('document', 'Already exists')

        return data

    def save(self):
        passenger = Passenger.objects.create(**self.cleaned_data)

        return modelToJson(model=passenger)

    def getErrors(self):
        return getErrorsFormatted(self)

class PassengerFindOneForm():
    errors = {}

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        if 'id' in params:
            self.instance = Passenger.objects.filter(id=params['id'])
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

class PassengerStateChangeForm(forms.Form):
    id = forms.IntegerField(required=True)
    active = forms.IntegerField(min_value=0,max_value=1,required=True)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = Passenger.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()
        
        return data

    def save(self):
        data = self.cleaned_data

        passenger = self.instance
        passenger.is_whitelist = data['active']

        passenger.save()

        return modelToJson(model=passenger)

    def getErrors(self):
        return getErrorsFormatted(self)