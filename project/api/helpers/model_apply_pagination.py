import math

def model_apply_pagination(query, params):

    limit = params['limit']
    offset = int(params['offset'])

    list = query[offset:limit]

    records_filtered = list.count()

    return {
        'page': offset,
        'current_page': offset,
        'per_page' : limit,
        'last_page': math.ceil(records_filtered / limit),
        'next_page': offset + 1 if (offset < records_filtered / limit) else None,
        'prev_page': offset - 1 if (offset > 1) else None,
        'list': list.all().values(),
    }
