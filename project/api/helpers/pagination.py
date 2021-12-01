def paginate_queryset(request):

    params = request.get_full_path()
    params = params.split('?')
    dict = {}
    if len(params) > 1:
        params = params[1].split('&')
        for param in params:
            param = param.split('=')
            dict[param[0]] = param[1].replace('%20' , ' ').strip() if 2 == len(param) else ''
    
    per_page = dict['per_page'] if 'per_page' in dict else None
    page = dict['page'] if 'page' in dict else None
    sort_by = dict['sort_by'] if 'sort_by' in dict else None
    sort = dict['sort'] if 'sort' in dict else None
    filter_by = dict['filter_by'] if 'filter_by' in dict else None
    filtrate = dict['filter'] if 'filter' in dict else None

    if not per_page:
        per_page = 10
    else:
        if per_page.isdigit():
            if int(per_page) > 0:
                per_page = int(per_page)
            else:
                per_page = 10
        else:
            per_page = 10
    
    if page is None:
        page = 1
    else:
        if (page) or (page.isdigit()):
            if int(page) > 0:
                page = int(page)
            else:
                page = 1
        else:
            page = 1

    if (sort_by is None) or (not sort_by):
        sort_by = 'created_at'

    if (sort is None) or (not sort):
        sort = 'asc'

    if (filter_by is None or filtrate is None) or (not filter_by or not filtrate):
        filter_by = False
        filtrate = False
    
    dict['limit'] = per_page
    dict['page'] = page
    dict['offset'] = (page - 1) * per_page

    dict['sort_by'] = sort_by
    dict['sort'] = sort

    dict['filter_by'] = filter_by
    dict['filter'] = filtrate

    return dict