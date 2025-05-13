from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import OrganizationFilters
from .models import Organization
from .serializers import OrganizationCreateSerializer, OrganizationSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all().prefetch_related(
        "addresses__location__parent_location__parent_location",
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrganizationFilters

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return OrganizationCreateSerializer
        return OrganizationSerializer
