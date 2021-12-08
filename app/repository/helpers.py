import json

def getErrorsFormatted(self):

    errors = json.loads(self._errors.as_json())

    errors_list = {}

    for key in errors:
        errors_list[key] = []
        for error in errors[key]:
            errors_list[key].append(error['message'])

    return errors_list

def modelToJson(model):
    
    dictionary = {}

    fields = model._meta.fields
    for field in fields:
        if field.name == 'id':
            dictionary['id'] = model.id
        else:
            value = getattr(model, field.name)
            if str(type(value)).find('app.models.') != -1:
                value = modelToJson(value)
            
            dictionary[field.name] = value

    return dictionary