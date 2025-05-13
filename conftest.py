import pytest
from itertools import cycle

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from model_bakery import baker, seq
from model_bakery.recipe import Recipe
from crum import set_current_user
import django

django.setup()


@pytest.fixture(name="user")
def fixture_user():
    from django.contrib.auth import get_user_model

    custom_user = Recipe(
        get_user_model(),
        email=seq("test@example.com"),
        first_name="Jan",
        last_name="Kowalski",
    )
    try:
        return custom_user.make()
    except IntegrityError:
        return custom_user.make()


@pytest.fixture(name="auth_client")
def fixture_auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    set_current_user(user)
    yield client
    set_current_user(None)


@pytest.fixture(name="address_kind")
def fixture_address_kind():
    return baker.make(
        "common.AddressKind",
        id=seq("id_"),
        kind=seq("kind_"),
        _quantity=2,
    )


@pytest.fixture(name="currency")
def fixture_currency():
    return baker.make(
        "common.Currency",
        code=cycle(["PLN", "EUR"]),
        name=cycle(["Polish Zloty", "Euro"]),
        _quantity=2,
    )


@pytest.fixture(name="location")
def fixture_location():
    return baker.make(
        "common.Location",
        name=cycle(["Poland", "Poznan"]),
        code=cycle(["PL", "POZ"]),
        location_kind=cycle(["CR", "CT"]),
        parent_location=None,
        _quantity=2,
    )


@pytest.fixture(name="organization")
def fixture_organization(location, address_kind):
    address = baker.make(
        "organizations.Address",
        address="address",
        zip_code="zip",
        location=location[0],
        kind=address_kind[0],
    )
    organization = baker.make(
        "organizations.Organization",
        addresses=[address],
        name=seq("name_"),
        nip=seq("nip_"),
        regon=seq("regon_"),
        krs=seq("krs_"),
        _quantity=2,
    )
    return {"organization": organization, "address_kind": address_kind}


@pytest.fixture(name="bank_account")
def fixture_bank_account(organization, currency):
    bank_account = baker.make(
        "common.BankAccount",
        number=seq("number_"),
        currency=currency[0],
        organization=organization["organization"][0],
        is_active=True,
        main_account=False,
        _quantity=2,
    )
    return bank_account
