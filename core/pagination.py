import re

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        current_page_number = self.page.number
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()

        if next_link:
            next_link = '/{}'.format(next_link.split('/', 3)[-1])
        if previous_link:
            previous_link = '/{}'.format(previous_link.split('/', 3)[-1])

        first_page = re.sub(
            r'\?page=\d+', '', previous_link) if previous_link else None
        last_page = re.sub(
            r'\?page=\d+', '?page={}'.format(
                self.page.paginator.num_pages
            ), next_link) if next_link else None

        return Response({
            'count': self.page.paginator.count,
            'first_page': first_page,
            'last_page': last_page,
            'next': next_link,
            'previous': previous_link,
            'last_page_number': self.page.paginator.num_pages,
            'current_page': current_page_number,
            'results': data,
        })
