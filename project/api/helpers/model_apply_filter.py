from .model_fields_types import model_fields_types
from datetime import datetime, timedelta
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

            tz_in_minutes = params['tz_in_minutes']
            
            if tz_in_minutes.isnumeric():
                tz_in_minutes = int(params['tz_in_minutes'])
            else:
                if tz_in_minutes.startswith("-") and tz_in_minutes[1:].isdigit():
                    tz_in_minutes = int(tz_in_minutes) # * -1:
                else:
                    tz_in_minutes = 0

            try:
                datetime_fomatted = datetime.strptime(filter_value, '%Y-%m-%d %H:%M:%S')

                datetime_with_tz = datetime_fomatted + timedelta(minutes=tz_in_minutes)

                query = query.filter(**{filters['filter_by']: datetime_with_tz})
            except ValueError:
                print('ValueError:', ValueError)
                pass

        else:
            query = query.filter(**{filters['filter_by']: filters['filter']})

    return query
