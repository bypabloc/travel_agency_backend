from django import forms
from ..models import Seat, JourneyDriver, Ticket, Q
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
            seat_x = int(data['seat_x'])
            if seat_x > 3:
                self.add_error('seat_x', 'X must be less than 3')
            else:
                seat_y = data['seat_y']
                seat_filter = Seat.objects.filter(
                    seat_x=seat_x,
                    seat_y__icontains=seat_y,
                )
                if seat_filter.exists():
                    self.add_error('seat_x', 'Seat already exists')
                    self.add_error('seat_y', 'Seat already exists')

        if Seat.objects.filter(
                is_active=1,
            ).count() >= 10:
                self.add_error('seat_x', 'The maximum number of active seats is 10')
                self.add_error('seat_y', 'The maximum number of active seats is 10')
        
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
        return modelToJson(model=self.instance.all().first())

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
        
        if 'active' in data:
            if data['active'] == 1:
                if Seat.objects.filter(
                        is_active=1,
                    ).count() >= 10:
                        self.add_error('active', 'The maximum number of active seats is 10')
        
        return data

    def save(self):
        data = self.cleaned_data

        seat = self.instance
        seat.is_active = data['active']

        seat.save()

        return modelToJson(model=seat)

    def getErrors(self):
        return getErrorsFormatted(self)

class SeatListAvailabilityForm():
    errors = {}
    seats_availability = []

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        journey_driver = False
        tickets = False
        if not 'journey_driver' in params:
            self.add_error('journey_driver', 'Field is required')
        else:
            journey_driver = JourneyDriver.objects.filter(id=params['journey_driver'])
            if not journey_driver.exists():
                self.add_error(field='journey_driver', error='Not exists')
            else:
                journey_driver = journey_driver.first()
                tickets = [item[0] for item in Ticket.objects.filter(journey_driver=journey_driver).all().values_list('seat_id')]


        if journey_driver:
            seats = Seat.objects.filter(
                is_active=1,
            ).all().values('id', 'seat_x', 'seat_y')
            for seat in seats:
                is_available = True
                if seat['id'] in tickets:
                    is_available = False

                self.seats_availability.append({
                    **seat,
                    'is_available': is_available,
                })

        return False if len(self.errors) > 0 else True

    def list(self):
        return self.seats_availability

    def add_error(self, field, error):
        if field in self.errors:
            self.errors[field].append(error)
        else:
            self.errors[field] = [error]

    def getErrors(self):
        return self.errors