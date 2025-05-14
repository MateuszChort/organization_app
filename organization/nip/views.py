from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .regon_api import nip_search


@api_view(["GET"])
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def get_data_by_nip(request, nip: int):
    result = nip_search(nip)
    if "ErrorCode" in result[0]:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)
