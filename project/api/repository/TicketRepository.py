from django import forms
from ..models import Ticket, Passenger, JourneyDriver, Seat

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination

class TicketListForm():
    def list(self):
        params = paginate_queryset(self.request)

        tickets = Ticket.objects

        tickets = model_apply_filter(model=Ticket, query=tickets, params=params)
        tickets = model_apply_sort(model=Ticket, query=tickets, params=params)
        tickets = model_apply_pagination(query=tickets, params=params)

        list = tickets['list'].all()

        list_formatted = []
        for item in list:
            list_formatted.append(modelToJson(item))

        tickets['list'] = list_formatted

        return tickets

class TicketCreateForm(forms.Form):
    states = forms.IntegerField(min_value=1, max_value=3, required=False)
    passenger = forms.IntegerField()
    journey_driver = forms.IntegerField()
    seat = forms.IntegerField()

    def clean(self):
        data = self.cleaned_data



        passenger = False
        if 'passenger' in data:
            passenger = Passenger.objects.filter(id=data['passenger'])
            if not passenger.exists():
                self.add_error('passenger', 'Does not exist')
            else:
                passenger = passenger.first()
                self.cleaned_data['passenger'] = passenger

        journey_driver = False
        if 'journey_driver' in data:
            journey_driver = JourneyDriver.objects.filter(id=data['journey_driver'])
            if not journey_driver.exists():
                self.add_error('journey_driver', 'Does not exist')
            else:
                journey_driver = journey_driver.first()
                self.cleaned_data['journey_driver'] = journey_driver

        seat = False
        if 'seat' in data:
            seat = Seat.objects.filter(id=data['seat'])
            if not seat.exists():
                self.add_error('seat', 'Does not exist')
            else:
                seat = seat.first()
                self.cleaned_data['seat'] = seat
        
        if passenger and journey_driver and seat:
            ticket = Ticket.objects.filter()
            if ticket.filter(
                passenger=passenger, 
                journey_driver=journey_driver, 
                seat=seat,
            ).exists():
                self.add_error('passenger', 'The ticket already exists')
                self.add_error('journey_driver', 'The ticket already exists')
                self.add_error('seat', 'The ticket already exists')
            elif ticket.filter(
                journey_driver=journey_driver,
                seat=seat,
            ).exists():
                self.add_error('journey_driver', 'The seat is already taken')
                self.add_error('seat', 'The seat is already taken')
            elif ticket.filter(
                journey_driver=journey_driver,
                passenger=passenger,
            ).exists():
                self.add_error('journey_driver', 'The passenger is already assigned')
                self.add_error('passenger', 'The passenger is already assigned')
        #     self.add_error('passenger', '')

        # self.add_error('passenger', 'Passenger, JourneyDriver or Seat is required')

        return data

    def save(self):
        ticket = Ticket.objects.create(**self.cleaned_data)

        return modelToJson(model=ticket)

    def getErrors(self):
        return getErrorsFormatted(self)

class TicketFindOneForm():
    errors = {}

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        if 'id' in params:
            self.instance = Ticket.objects.filter(id=params['id'])
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

class TicketStateChangeForm(forms.Form):
    id = forms.IntegerField()
    states = forms.IntegerField(min_value=1, max_value=3)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = Ticket.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()
        
        return data

    def save(self):
        data = self.cleaned_data

        ticket = self.instance
        ticket.states = data['states']

        ticket.save()

        return modelToJson(model=ticket)

    def getErrors(self):
        return getErrorsFormatted(self)

class TicketSeatChangeForm(forms.Form):
    id = forms.IntegerField()
    seat = forms.IntegerField()

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = Ticket.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()

        seat = False
        if 'seat' in data:
            seat = Seat.objects.filter(id=data['seat'])
            if not seat.exists():
                self.add_error('seat', 'Does not exist')
            else:
                seat = seat.first()
                self.cleaned_data['seat'] = seat
                if seat.id == self.instance.seat.id:
                    self.add_error('seat', 'Must indicate another seat.')

        return data

    def save(self):
        data = self.cleaned_data

        ticket = self.instance
        ticket.states = data['states']

        ticket.save()

        return modelToJson(model=ticket)

    def getErrors(self):
        return getErrorsFormatted(self)