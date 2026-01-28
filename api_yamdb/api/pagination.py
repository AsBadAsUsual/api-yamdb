from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 5

    def get_paginated_response(self, data):

        if (self.request.query_params.get('limit') is None
                and self.request.query_params.get('offset') is None):
            return Response(data)
        else:
            return Response({
                'count': self.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            })
