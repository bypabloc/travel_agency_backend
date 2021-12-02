from django import forms
from ..models import Seat
from django.core.validators import RegexValidator

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination

only_character = RegexValidator(r'^[a-zA-Z]*$', 'Only characters are allowed.')
only_numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')

class SeatListForm():
    def list(self):
        params = paginate_queryset(self.request)

        seats = Seat.objects

        seats = model_apply_filter(model=Seat, query=seats, params=params)
        seats = model_apply_sort(model=Seat, query=seats, params=params)
        seats = model_apply_pagination(query=seats, params=params)

        list = seats['list'].all()

        list_formatted = []
        for item in list:
            list_formatted.append(modelToJson(item))

        seats['list'] = list_formatted

        return seats

class SeatCreateForm(forms.Form):
    seat_x = forms.CharField(max_length=1, validators=[only_numeric])
    seat_y = forms.CharField(max_length=1, validators=[only_character])
    is_active = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data
        
        if 'seat_x' in data and 'seat_y' in data:
            if Seat.objects.filter(
                seat_x=data['seat_x'], 
                seat_y=data['seat_y']
            ).exists():
                self.add_error('seat_x', 'Seat already exists')
                self.add_error('seat_y', 'Seat already exists')
        
        return data

    def save(self):
        seat = Seat.objects.create(**self.cleaned_data)
        return modelToJson(model=seat)

    def getErrors(self):
        return getErrorsFormatted(self)

class SeatFindOneForm():
    errors = {}

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        if 'id' in params:
            self.instance = Seat.objects.filter(id=params['id'])
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

class SeatStateChangeForm(forms.Form):
    id = forms.IntegerField(required=True)
    active = forms.IntegerField(min_value=0,max_value=1,required=True)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = Seat.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()
        
        return data

    def save(self):
        data = self.cleaned_data

        seat = self.instance
        seat.is_active = data['active']

        seat.save()

        return modelToJson(model=seat)

    def getErrors(self):
        return getErrorsFormatted(self)