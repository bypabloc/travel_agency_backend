
    # param1 = request.GET['param1']
    # param2 = request.GET['param2']
    # param1 = request.GET.get('param1')
    # param2 = request.GET.get('param2')
def paginate_queryset(request):

    per_page = request.GET.get('per_page')
    page = request.GET.get('page')
    sort_by = request.GET.get('sort_by')
    sort = request.GET.get('sort')
    filter_by = request.GET.get('filter_by')
    filtrate = request.GET.get('filter')

    if per_page is None:
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
        if page.isdigit():
            if int(page) > 0:
                page = int(page)
            else:
                page = 1
        else:
            page = 1

    if (sort_by is None) or (not sort_by):
        sort_by = 'id'

    if (sort is None) or (not sort):
        sort = 'asc'

    if (filter_by is None or filtrate is None) or (not filter_by or not filtrate):
        filter_by = False
        filtrate = False

    return {
        'per_page' : per_page,
        'page' : page,
        'offset' : (page - 1) * per_page,

        'sort_by' : sort_by,
        'sort' : sort,
        'filter_by' : filter_by,
        'filtrate' : filtrate,
    }


# export default async (req, res, next) => {
#     try {
#         const { per_page, page } = req.body;

#         const per_page_formatted = per_page ? (per_page > 0 ? per_page : 10) : 10;
#         const page_formatted = ( page ? (page < 0 ? 1 : page) : 1 );
        
#         req['pagination'] = {
#             page: page_formatted,
#             per_page: per_page_formatted,
#             offset: (page_formatted - 1) * per_page_formatted,
#         }

#         next();
#     } catch(errors) {
#         console.log('Errors:', errors);
#         return response.sendUnprocessableEntity(res, { errors });
#     }
# };