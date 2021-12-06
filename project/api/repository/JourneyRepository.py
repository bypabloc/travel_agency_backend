from django import forms
from ..models import Journey, Location, Q
from rest_framework import serializers
from django.core import serializers as django_serializers
from rest_framework.renderers import JSONRenderer

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination

class JourneySerializer(serializers.Serializer):
    class Meta:
        model = Journey
        fields = '__all__'

class JourneyListForm():
    def list(self):
        params = paginate_queryset(self.request)

        journeys = Journey.objects
        
        journeys = journeys.average_passengers()

        journeys = model_apply_filter(model=Journey, query=journeys, params=params)
        if 'search' in params:
            journeys = journeys.filter(
                Q(location_origin__name__icontains=params['search']) |
                Q(location_destination__name__icontains=params['search'])
            )
            journeys = journeys.filter(
                is_active=True
            )
            print('journeys.query: ', journeys.query)
        journeys = model_apply_sort(model=Journey, query=journeys, params=params)
        journeys = model_apply_pagination(query=journeys, params=params)

        list = journeys['list'].all().values(
            "id",
            "location_origin_data",
            "location_destination_data",
            "duration_in_seconds",
            "is_active",
            "created_at",
            "updated_at",
            'average_passengers',
        )

        journeys['list'] = list

        # list = journeys['list'].all()

        # list_formatted = []
        # for item in list:
        #     list_formatted.append(modelToJson(item))

        # journeys['list'] = list_formatted

        return journeys

class JourneyCreateForm(forms.Form):
    duration_in_seconds = forms.IntegerField()
    location_origin = forms.IntegerField()
    location_destination = forms.IntegerField()
    is_active = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data

        if 'location_origin' in data:
            location_origin = Location.objects.filter(id=data['location_origin'])
            if not location_origin.exists():
                self.add_error('location_origin', 'Does not exist')
            else:
                self.cleaned_data['location_origin'] = location_origin.first()

        if 'location_destination' in data:
            location_destination = Location.objects.filter(id=data['location_destination'])
            if not location_destination.exists():
                self.add_error('location_destination', 'Does not exist')
            else:
                self.cleaned_data['location_destination'] = location_destination.first()

        if 'location_destination' in data and 'location_origin' in data:
            if data['location_destination'] == data['location_origin']:
                self.add_error('location_destination', 'Origin and destination must be different')
            elif Journey.objects.filter(
                    location_origin=data['location_origin'],
                    location_destination=data['location_destination'],
                ).exists():
                self.add_error('location_origin', 'Journey already exists')
                self.add_error('location_destination', 'Journey already exists')

        return data

    def save(self):
        journey = Journey.objects.create(**self.cleaned_data)

        return modelToJson(model=journey)

    def getErrors(self):
        return getErrorsFormatted(self)

class JourneyFindOneForm():
    errors = {}

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        if 'id' in params:
            self.instance = Journey.objects.filter(id=params['id'])
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

class JourneyStateChangeForm(forms.Form):
    id = forms.IntegerField(required=True)
    active = forms.IntegerField(min_value=0,max_value=1,required=True)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = Journey.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()
        
        return data

    def save(self):
        data = self.cleaned_data

        journey = self.instance
        journey.is_active = data['active']

        journey.save()

        return modelToJson(model=journey)

    def getErrors(self):
        return getErrorsFormatted(self)

