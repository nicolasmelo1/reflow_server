import math


class Pagination:
    def __init__(self, offset, limit, current_page, items_per_page):
        self.offset = offset
        self.limit = limit
        self.current_page = current_page
        self.items_per_page = items_per_page


    def get_total_number_of_pages(self, total_items):
        return math.ceil(total_items / self.items_per_page)

    @classmethod
    def handle_pagination(cls, current_page, items_per_page=25):
        pagination_limit = items_per_page * current_page
        pagination_offset = pagination_limit - items_per_page

        return cls(pagination_offset, pagination_limit, current_page, items_per_page)