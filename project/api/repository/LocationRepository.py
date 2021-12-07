from django import forms
from ..models import Location, Q

from .helpers import getErrorsFormatted, modelToJson
from ..helpers.pagination import paginate_queryset
from ..helpers.model_apply_sort import model_apply_sort
from ..helpers.model_apply_filter import model_apply_filter
from ..helpers.model_apply_pagination import model_apply_pagination

class LocationListForm():
    def list(self):
        params = paginate_queryset(self.request)

        locations = Location.objects
        
        if 'available' in params:
            locations = locations.available()
            print('locations.query: ', locations.query)

        locations = model_apply_filter(model=Location, query=locations, params=params)
        if 'search' in params:
            locations = locations.filter(
                Q(name__icontains=params['search'])
            )
            locations = locations.filter(
                is_active=True
            )

        locations = model_apply_sort(model=Location, query=locations, params=params)
        locations = model_apply_pagination(query=locations, params=params)

        list = locations['list'].all()

        list_formatted = []
        for item in list:
            list_formatted.append(modelToJson(item))

        locations['list'] = list_formatted

        return locations

class LocationCreateForm(forms.Form):
    name = forms.CharField(max_length=50)
    is_active = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data

        if 'name' in data:
            if Location.objects.filter(name=data['name']).exists():
                self.add_error('name', 'Already exists')
        
        return data

    def save(self):
        location = Location.objects.create(**self.cleaned_data)
        return modelToJson(model=location)

    def getErrors(self):
        return getErrorsFormatted(self)

class LocationFindOneForm():
    errors = {}

    def is_valid(self):
        self.errors = {}
        params = paginate_queryset(self.request)
        
        if 'id' in params:
            self.instance = Location.objects.filter(id=params['id'])
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

class LocationStateChangeForm(forms.Form):
    id = forms.IntegerField(required=True)
    active = forms.IntegerField(min_value=0,max_value=1,required=True)

    def clean(self):
        data = self.cleaned_data

        if 'id' in data:
            self.instance = Location.objects.filter(id=data['id'])
            if not self.instance.exists():
                self.add_error('id', 'Not exists')
            else:
                self.instance = self.instance.first()
        
        return data

    def save(self):
        data = self.cleaned_data

        location = self.instance
        location.is_active = data['active']

        location.save()

        return modelToJson(model=location)

    def getErrors(self):
        return getErrorsFormatted(self)