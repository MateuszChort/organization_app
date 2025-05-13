from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import AddressKind, BankAccount, Currency, Location
from .serializers import (
    AddressKindSerializer,
    BankAccountCreateUpdateSerializer,
    BankAccountSerializer,
    CurrencySerializer,
    LocationCreateUpdateSerializer,
    LocationSerializer,
)


class AddressKindViewSet(ModelViewSet):
    queryset = AddressKind.objects.all()
    serializer_class = AddressKindSerializer


class CurrencyViewSet(ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all().prefetch_related(
        "parent_location__parent_location__parent_location",
    )
    serializer_class = LocationSerializer
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ["location_kind", "parent_location"]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "code"]

    def get_serializer_class(self):
        if self.action == "list":
            return LocationSerializer
        return LocationCreateUpdateSerializer


class BankAccountViewSet(ModelViewSet):
    queryset = (
        BankAccount.objects.all()
        .select_related("organization")
        .prefetch_related("currency")
    )

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "organization_id",
        "number",
    )

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return BankAccountSerializer
        return BankAccountCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            BankAccountSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )
