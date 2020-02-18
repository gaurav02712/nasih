from flask import request, g, url_for
from sqlalchemy import desc, asc, event
from sqlalchemy_filters import apply_filters

PAGE = 1
LIMIT = 10
IS_DELETED = True
IS_NOT_DELETED = False
STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
STATUS_DELETED = 10


class UserCreatedMixin(object):
    @staticmethod
    def get_created_by(mapper, connection, target):
        target.created_by = g.user_id
        target.updated_by = g.user_id

    @staticmethod
    def get_updated_by(mapper, connection, target):
        target.updated_by = g.user_id

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_insert', cls.get_created_by)
        event.listen(cls, 'before_update', cls.get_updated_by)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
        to any declarative-mapped class.
    """

    @classmethod
    def get_by_id(cls, record_id):
        """
        Get record by ID.
        :param record_id: Id from which data have to find
        :param deleted: Accepts Boolean to get deleted or not deleted data
        :param status: Accepts small int to get active or inactive data
        :return:
        """
        # if any(
        #         (isinstance(record_id, basestring) and record_id.isdigit(),
        #          isinstance(record_id, (int, float))),
        # ):
        if record_id is None:
            return None
        return cls.query.filter_by(id=int(record_id)).first()
        # return cls.query.filter_by(id=int(record_id), is_deleted=deleted, status=status).first()

    @classmethod
    def find_all(cls, pagination: bool = False, deleted: bool = IS_NOT_DELETED, page=PAGE, limit=LIMIT,
                 filter_spec=None, **kwargs):
        # @classmethod
        # def find_all(cls, pagination: bool = False, deleted: bool = IS_NOT_DELETED,
        #              status: int = STATUS_ACTIVE, page=PAGE, limit=LIMIT, filter_spec=None, **kwargs):
        order = desc
        orderby = request.args.get('orderby')
        if orderby == 'asc':
            order = asc
        column_name = request.args.get('column', 'id')
        """Get record by ALL.

        :param pagination:
        :param deleted:
        :param status:
        :param page:
        :param limit:
        :return:
        """

        # TODO:- @kafeel need to discuess

        status = kwargs['status'] if 'status' in kwargs else None
        if hasattr(cls, 'status') and status is not None:  # to get all status
            kwargs.update(status=status)
        else:
            kwargs.pop('status', None)
            if hasattr(cls, 'is_deleted'):
                kwargs.update(is_deleted=deleted)

        res = cls.query.filter_by(**kwargs)
        if filter_spec:
            res = apply_filters(res, filter_spec)
        if hasattr(g, 'filter_condition'):
            res = cls.filter_query(res, g.filter_condition)
        # if args:
        #     res = res.filter(and_(*args))

        res = res.order_by(order(column_name))

        # if pagination:
        #     res = res.filter(Article.tagList.any(Tags.tagname == tag))

        if pagination:
            res = res.paginate(page, limit, error_out=True)
        else:
            res = res.all()
        return res

    @classmethod
    def count(cls, status=STATUS_ACTIVE, **kwargs):
        """Get count of record
        """
        kwargs.update(is_deleted=IS_NOT_DELETED, status=status)
        res = cls.query.filter_by(**kwargs)

        return res.count()

    # @classmethod
    # def delete(cls, record_id: int):
    #     """Deleted an Object """
    #     return cls.query.filter_by(id=int(record_id)).first()

    @classmethod
    def filter_query(cls, query, filter_condition):
        from sqlalchemy import or_
        '''
        Return filtered queryset based on condition.
        :param query: takes query
        :param filter_condition: Its a list, ie: [(key,operator,value)]
        operator list:
            eq for ==
            lt for <
            ge for >=
            in for in_
            like for like
            value could be list or a string
        :return: queryset

        '''

        model_class = cls  # returns the query's Model
        for key, value in filter_condition.items():
            column = getattr(model_class, key, None)
            if column and value != '' and value is not None:
                if isinstance(value, list):
                    if key == 'category_id':
                        cat = []
                        from sqlalchemy import type_coerce
                        for a in value:
                            cat.append(column.cast(db.String) == type_coerce([a], db.JSON))
                        filt = or_(*cat)

                    else:
                        filt = column.in_(value)
                else:
                    ope = 'eq'
                    if type(value) is str:
                        ope = 'like'
                    try:
                        attr = list(filter(
                            lambda e: hasattr(column, e % ope),
                            ['%s', '%s_', '__%s__']
                        ))[0] % ope
                    except IndexError:
                        raise Exception('Invalid filter operator: %s' % ope)
                    if value == 'null':
                        value = None
                    filt = getattr(column, attr)(value)
                # if key != 'category_id':
                query = query.filter(filt)
        return query
