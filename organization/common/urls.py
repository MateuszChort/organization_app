from rest_framework import routers

from .views import (
    AddressKindViewSet,
    BankAccountViewSet,
    CurrencyViewSet,
    LocationViewSet,
)

router = routers.DefaultRouter()
router.register(r"address_kind", AddressKindViewSet)
router.register(r"currency", CurrencyViewSet)
router.register(r"location", LocationViewSet)
router.register(r"bank_account", BankAccountViewSet)
