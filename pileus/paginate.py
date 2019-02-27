from math import ceil

class NoDataInPage(Exception):
    def __init__(self):
        super().__init__('No Data In this Page')

class Paginate(object):
    def __init__(self, query, page, per_page, total, items):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def prev_num(self):
        return self.has_prev and self.page - 1 or None

    @property
    def has_prev(self):
        return self.page > 1

    def next(self, error_out = False):
        if not self.query:
            return None
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        return self.has_next and self.page + 1 or None

    @property
    def p(self):
        return {
            'has_next': self.has_next,
            'has_prev': self.has_prev,
            'next_num': self.next_num,
            'page': self.page,
            'pages': self.pages,
            'prev_num': self.prev_num,
            'total': self.total
        }


def paginate(query, page = 1, per_page = 20, error_out = False):
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    if not items and page !=1 and error_out:
        raise NoDataInPage()
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.object_by(None).count()
    return Paginate(query, page, per_page, total, items)