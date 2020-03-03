from math import ceil
from flask import request
from api.config.constants import K


def get_paginated_list(paginator, schema, limit=K.PAGINATION_PER_PAGE):
    obj = {}
    if schema.many is True:
        obj['limit'] = paginator.per_page
        obj['total'] = paginator.total
        obj['total_pages'] = ceil(paginator.total / limit)
        # make previous url
        if paginator.has_prev:
            obj['previous'] = request.url + '?page=%d&limit=%d' % (paginator.prev_num, limit)
        # make next url
        if paginator.has_next:
            obj['next'] = request.url + '?page=%d&limit=%d' % (paginator.next_num, limit)
        paginator = paginator.items
        # finally extract result according to bounds
    obj['results'] = schema.dump(paginator)
    return obj


# def pagination_kwargs(request) -> dict:
#     page = request.values.get('page', PAGE, type=int)
#     limit = request.values.get('limit', LIMIT, type=int)
#     kwargs = {'pagination': True, 'page': page, 'limit': limit}
#     status = request.args.get('status', None, type=int)
#     if status is not None:
#         kwargs.update({'status': StatusType.ACTIVE.value})
#     return kwargs
