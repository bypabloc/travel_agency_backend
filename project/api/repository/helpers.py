import json

def getErrorsFormatted(self):

    errors = json.loads(self._errors.as_json())

    errors_list = {}

    for key in errors:
        errors_list[key] = []
        for error in errors[key]:
            errors_list[key].append(error['message'])

    return errors_list
