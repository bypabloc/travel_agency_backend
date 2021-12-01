from django.db.models.functions import Lower
from .model_fields_types import model_fields_types

def model_apply_filter(model, query, params):

    fields = model_fields_types(model=model)

    filters = {}

    filter_by = params['filter_by']

    if filter_by in fields:
        print('filter_by: ', filter_by)

        filters[filter_by] = params['filter']
    
    return query.filter(**filters)
