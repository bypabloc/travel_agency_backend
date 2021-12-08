from .pagination import paginate_queryset

def get_request_tz(request):
    
    params = paginate_queryset(request)

    tz_in_minutes = params['tz_in_minutes']
    
    if tz_in_minutes.isnumeric():
        tz_in_minutes = int(params['tz_in_minutes'])
    else:
        if tz_in_minutes.startswith("-") and tz_in_minutes[1:].isdigit():
            tz_in_minutes = int(tz_in_minutes) # * -1:
        else:
            tz_in_minutes = 0

    return tz_in_minutes
