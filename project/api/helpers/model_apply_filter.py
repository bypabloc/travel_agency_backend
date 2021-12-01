from .model_fields_types import model_fields_types
from datetime import datetime
import pytz

def model_apply_filter(model, query, params):

    fields = model_fields_types(model=model)

    filters = {}

    filter_by = params['filter_by']

    if filter_by in fields:
        filters['filter_by'] = filter_by
        filters['filter'] = params['filter']
        filters['type'] = fields[filter_by]
    
    print('filters:', filters)
    print('fields:', fields)

    if 'filter_by' in filters and 'filter' in filters:
        if filters['type'] == 'CharField':
            query = query.extra(where=[''+filters['filter_by']+' LIKE %s'], params=['%'+filters['filter']+'%'])
        
        elif filters['type'] == 'IntegerField' or filters['type'] == 'BigIntegerField' or filters['type'] == 'BigAutoField':
            filter_value = filters['filter']
            if filter_value.isdigit():
                query = query.filter(**{filters['filter_by']: int(filter_value)})

        elif filters['type'] == 'DateTimeField':
            filter_value = filters['filter']

            try:
                datetima_fomatted = datetime.strptime(filter_value, '%Y-%m-%d %H:%M:%S')
                dt_utc = datetima_fomatted.astimezone(pytz.UTC)
                query = query.filter(**{filters['filter_by']: dt_utc})
            except ValueError:
                print('ValueError:', ValueError)
                pass

        else:
            query = query.filter(**{filters['filter_by']: filters['filter']})

    return query
