import pytest
from rest_framework import status

from organization.common.models import AddressKind, BankAccount, Currency, Location
from organization.utils import remove_ids


@pytest.mark.django_db
def test_address_kind_list(auth_client, address_kind):
    response = auth_client.get("/api/common/address_kind/")
    expected_response = [
        {"id": "id_1", "kind": "kind_1"},
        {"id": "id_2", "kind": "kind_2"},
    ]
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_address_kind_retrieve(auth_client, address_kind):
    response = auth_client.get(f"/api/common/address_kind/{address_kind[0].id}/")
    expected_response = {"id": "id_1", "kind": "kind_1"}
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_address_kind_create(auth_client):
    data = {"id": "new_address_kind_id", "kind": "new_kind"}
    response = auth_client.post("/api/common/address_kind/", data=data)
    expected_response = {"id": "new_address_kind_id", "kind": "new_kind"}
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_response


@pytest.mark.django_db
def test_address_kind_update(auth_client, address_kind):
    data = {"id": "updated_id", "kind": "updated_kind"}
    response = auth_client.put(
        f"/api/common/address_kind/{address_kind[0].id}/", data=data
    )
    expected_response = {"id": "updated_id", "kind": "updated_kind"}
    assert response.data == expected_response
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_address_kind_delete(auth_client, address_kind):
    address_kind = AddressKind.objects.get(id=address_kind[0].id)
    response = auth_client.delete(f"/api/common/address_kind/{address_kind.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(AddressKind.DoesNotExist):
        address_kind.refresh_from_db()


@pytest.mark.django_db
def test_bank_account_list(auth_client, bank_account):
    response = auth_client.get("/api/common/bank_account/")
    expected_response = [
        {
            "number": "number_1",
            "currency": {"code": "PLN", "name": "Polish Zloty"},
            "organization": {
                "name": "name_1",
                "addresses": [
                    {
                        "location": {
                            "name": "Poland",
                            "parent_location": None,
                            "code": "PL",
                            "location_kind": "CR",
                        },
                        "kind": "id_1",
                        "zip_code": "zip",
                        "address": "address",
                    }
                ],
                "nip": "nip_1",
                "regon": "regon_1",
                "krs": "krs_1",
            },
            "is_active": True,
            "main_account": False,
        },
        {
            "number": "number_2",
            "currency": {"code": "PLN", "name": "Polish Zloty"},
            "organization": {
                "name": "name_1",
                "addresses": [
                    {
                        "location": {
                            "name": "Poland",
                            "parent_location": None,
                            "code": "PL",
                            "location_kind": "CR",
                        },
                        "kind": "id_1",
                        "zip_code": "zip",
                        "address": "address",
                    }
                ],
                "nip": "nip_1",
                "regon": "regon_1",
                "krs": "krs_1",
            },
            "is_active": True,
            "main_account": False,
        },
    ]
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_bank_account_retrieve(auth_client, bank_account):
    response = auth_client.get(f"/api/common/bank_account/{bank_account[0].id}/")
    expected_response = {
        "number": "number_1",
        "currency": {"code": "PLN", "name": "Polish Zloty"},
        "organization": {
            "name": "name_1",
            "addresses": [
                {
                    "location": {
                        "name": "Poland",
                        "parent_location": None,
                        "code": "PL",
                        "location_kind": "CR",
                    },
                    "kind": "id_1",
                    "zip_code": "zip",
                    "address": "address",
                }
            ],
            "nip": "nip_1",
            "regon": "regon_1",
            "krs": "krs_1",
        },
        "is_active": True,
        "main_account": False,
    }
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_bank_account_create(auth_client, currency):
    post_parameters = {
        "number": "new_number",
        "currency": currency[0].code,
        "is_active": True,
        "main_account": False,
    }
    response = auth_client.post("/api/common/bank_account/", post_parameters)
    expected_response = {
        "number": "new_number",
        "currency": {"code": "PLN", "name": "Polish Zloty"},
        "organization": None,
        "is_active": True,
        "main_account": False,
    }
    assert response.status_code == status.HTTP_201_CREATED
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_bank_account_update(auth_client, bank_account):
    data = {
        "number": "updated_number",
        "currency": bank_account[0].currency.code,
        "is_active": False,
        "main_account": True,
    }
    response = auth_client.put(
        f"/api/common/bank_account/{bank_account[0].id}/", data=data
    )
    expected_response = {
        "number": "updated_number",
        "currency": bank_account[0].currency.code,
        "organization": bank_account[0].organization.id,
        "is_active": False,
        "main_account": True,
    }
    assert response.data == expected_response
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_bank_account_delete(auth_client, bank_account):
    bank_account = BankAccount.objects.get(id=bank_account[0].id)
    response = auth_client.delete(f"/api/common/bank_account/{bank_account.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(BankAccount.DoesNotExist):
        bank_account.refresh_from_db()


@pytest.mark.django_db
def test_currency_list(auth_client, currency):
    response = auth_client.get("/api/common/currency/")
    expected_response = [
        {"code": "PLN", "name": "Polish Zloty"},
        {"code": "EUR", "name": "Euro"},
    ]
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_currency_retrieve(auth_client, currency):
    response = auth_client.get(f"/api/common/currency/{currency[0].code}/")
    expected_response = {"code": "PLN", "name": "Polish Zloty"}
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_currency_create(auth_client):
    data = {"code": "USD", "name": "US Dollar"}
    response = auth_client.post("/api/common/currency/", data=data)
    expected_response = {"code": "USD", "name": "US Dollar"}
    assert response.status_code == status.HTTP_201_CREATED
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_currency_update(auth_client, currency):
    data = {"code": "CHF", "name": "Frank"}
    response = auth_client.put(f"/api/common/currency/{currency[0].code}/", data=data)
    expected_response = {"code": "CHF", "name": "Frank"}
    assert response.data == expected_response
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_currency_delete(auth_client, currency):
    currency = Currency.objects.get(code=currency[0].code)
    response = auth_client.delete(f"/api/common/currency/{currency.code}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Currency.DoesNotExist):
        currency.refresh_from_db()


@pytest.mark.django_db
def test_location_list(auth_client, location):
    response = auth_client.get("/api/common/location/")
    expected_response = [
        {
            "name": "Poland",
            "parent_location": None,
            "code": "PL",
            "location_kind": "CR",
        },
        {
            "name": "Poznan",
            "parent_location": None,
            "code": "POZ",
            "location_kind": "CT",
        },
    ]
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_location_retrieve(auth_client, location):
    response = auth_client.get(f"/api/common/location/{location[0].id}/")
    expected_response = {
        "name": "Poland",
        "parent_location": None,
        "code": "PL",
        "location_kind": "CR",
    }
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_location_create(auth_client):
    post_parameters = {
        "name": "New Location",
        "parent_location": None,
        "code": "NL",
        "location_kind": "CR",
    }
    response = auth_client.post("/api/common/location/", post_parameters, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert remove_ids(response.data) == post_parameters


@pytest.mark.django_db
def test_location_create_with_parent(auth_client, location):
    post_parameters = {
        "name": "New Location with Parent",
        "parent_location": location[0].id,
        "code": "NLP",
        "location_kind": "CT",
    }
    response = auth_client.post("/api/common/location/", post_parameters, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert remove_ids(response.data) == post_parameters


@pytest.mark.django_db
def test_location_update(auth_client, location):
    put_parameters = {
        "name": "Updated Location",
        "parent_location": None,
        "code": "UL",
        "location_kind": "CT",
    }
    response = auth_client.put(
        f"/api/common/location/{location[0].id}/", put_parameters, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == put_parameters


@pytest.mark.django_db
def test_location_update_with_same_parent(auth_client, location):
    location = Location.objects.get(id=location[0].id)
    location.parent_location = location
    location.save()
    put_parameters = {
        "name": "New Location with Same Parent",
        "parent_location": location.id,
        "code": "NLS",
        "location_kind": "CT",
    }
    response = auth_client.patch(
        f"/api/common/location/{location.id}/", put_parameters, format="json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "non_field_errors": ["Parent location cannot reference to the same object"]
    }


@pytest.mark.django_db
def test_location_delete(auth_client, location):
    location = Location.objects.get(id=location[0].id)
    response = auth_client.delete(f"/api/common/location/{location.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Location.DoesNotExist):
        location.refresh_from_db()
