from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()

        if next_link:
            next_link = '/{}'.format(next_link.split('/', 3)[-1])
        if previous_link:
            previous_link = '/{}'.format(previous_link.split('/', 3)[-1])

        return Response({
            'next': next_link,
            'previous': previous_link,
            'count': self.page.paginator.count,
            'results': data,
            'incomplete_results': (
                self.page.paginator.count > self.page.paginator.num_pages *
                self.page_size
            ),
        })
