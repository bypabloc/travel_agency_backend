from django import forms
from ..models import Bus
import json

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
        errors = json.loads(self._errors.as_json())

        errors_list = {}

        for key in errors:
            errors_list[key] = []
            for error in errors[key]:
                errors_list[key].append(error['message'])

        return errors_list

class AuthSignInForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

    def clean(self):
        data = self.cleaned_data

        print(data)

        user = Bus.objects.filter(email=data['email'])

        if not user.exists():
            self.add_error('email', 'Does not exist')

        user = user.first()

        return data

    def getErrors(self):
        errors = json.loads(self._errors.as_json())

        errors_list = {}

        for key in errors:
            errors_list[key] = []
            for error in errors[key]:
                errors_list[key].append(error['message'])

        return errors_list
