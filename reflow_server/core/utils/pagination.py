import math


class Pagination:
    def __init__(self, offset, limit, current_page, items_per_page):
        self.offset = offset
        self.limit = limit
        self.current_page = current_page
        self.items_per_page = items_per_page

    def paginate_queryset(self, queryset):
        """
        Recieves a queryset and paginate it with the data of the Pagination object.
        This returns a range of instances in the queryset based of and offset and an limit

        Args:
            queryset (django.db.QuerySet): A queryset you want to paginate

        Returns:
            tuple(int, django.db.QuerySet): Returns a tuple, with the first element being the number of pages and the second, 
                                            the queryset divided respecting the range defined.
        """
        total_number_of_pages = self.get_total_number_of_pages(queryset.count())
        return total_number_of_pages, queryset[self.offset: self.limit]
    
    def get_total_number_of_pages(self, total_items):
        return math.ceil(total_items / self.items_per_page)

    @classmethod
    def handle_pagination(cls, current_page, items_per_page=25):
        pagination_limit = items_per_page * current_page
        pagination_offset = pagination_limit - items_per_page

        return cls(pagination_offset, pagination_limit, current_page, items_per_page)