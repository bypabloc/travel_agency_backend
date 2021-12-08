from django.db.models.functions import Lower
from .model_fields_types import model_fields_types

def model_apply_sort(model, query, params):

    fields = model_fields_types(model=model)

    sort_by = params['sort_by']

    # query = query.extra(select={sort_by:'LOWER('+sort_by+')'})
    if sort_by in fields:
        if fields[sort_by] == 'CharField':
            if params['sort'] == 'asc':
                query = query.order_by(Lower(sort_by).asc())
            else:
                query = query.order_by(Lower(sort_by).desc())
        else:
            if params['sort'] == 'asc':
                query = query.order_by(sort_by)
            else:
                query = query.order_by('-'+sort_by)

    return query
