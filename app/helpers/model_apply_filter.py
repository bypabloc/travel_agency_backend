from .model_fields_types import model_fields_types
from datetime import datetime, timedelta

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

        elif filters['type'] == 'BooleanField' :
            filter_value = filters['filter']
            print('filter_value:', filter_value)
            if (
                filter_value == 'True' or 
                filter_value == 'true' or 
                filter_value == '1' or 
                filter_value == 'yes' or 
                filter_value == 'y' or 
                filter_value == 't' or 
                filter_value == 'T' or 
                filter_value == 'Y' or 
                filter_value == 'Yes' or 

                filter_value == 'False' or 
                filter_value == 'false' or 
                filter_value == '0' or 
                filter_value == 'no' or 
                filter_value == 'n' or 
                filter_value == 'f' or 
                filter_value == 'F' or 
                filter_value == 'N' or 
                filter_value == 'No'
            ):
                filters['filter'] = True;
                if (
                    filter_value == 'True' or 
                    filter_value == 'true' or 
                    filter_value == '1' or 
                    filter_value == 'yes' or 
                    filter_value == 'y' or 
                    filter_value == 't' or 
                    filter_value == 'T' or 
                    filter_value == 'Y' or 
                    filter_value == 'Yes'
                ):
                    filters['filter'] = True;
                else:
                    filters['filter'] = False;
                query = query.filter(**{filters['filter_by']: filters['filter']})

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
