from .model_fields_types import model_fields_types
import datetime

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

        print('filter_by:', filters['filter_by'])
        print('filter:', filters['filter'])
        print('type:', filters['type'])

        if filters['type'] == 'CharField':
            query = query.extra(where=[''+filters['filter_by']+' LIKE %s'], params=['%'+filters['filter']+'%'])
        
        elif filters['type'] == 'IntegerField' or filters['type'] == 'BigIntegerField' or filters['type'] == 'BigAutoField':
            filter_value = filters['filter']
            if filter_value.isdigit():
                query = query.filter(**{filters['filter_by']: int(filter_value)})

        elif filters['type'] == 'DateTimeField':
            filter_value = filters['filter']

            try:
                datetime.datetime.strptime(filter_value, '%Y-%m-%d %H:%M:%S')
                query = query.extra(where=[''+filters['filter_by']+' = %s'], params=[filters['filter']])
            except ValueError:
                pass

        else:
            query = query.filter(**{filters['filter_by']: filters['filter']})

    return query
