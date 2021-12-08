import math

def model_apply_pagination(query, params):

    limit = params['limit']
    offset = int(params['offset'])

    records_filtered = query.count()

    list = query[offset:offset+limit]

    return {
        'page': math.ceil(offset / limit + 1),
        'per_page' : limit,
        'records_total' : records_filtered,
        'last_page': math.ceil(records_filtered / limit),
        'next_page': offset + 1 if (offset < records_filtered / limit) else None,
        'prev_page': offset - 1 if (offset > 1) else None,
        'list': list.all()
    }