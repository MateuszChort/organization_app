import pytest
from rest_framework import status

from organization.organizations.models import Organization
from organization.utils import remove_ids


@pytest.mark.django_db
def test_organization_list(auth_client, organization):
    response = auth_client.get("/api/organizations/")
    expected_response = [
        {
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
        {
            "name": "name_2",
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
            "nip": "nip_2",
            "regon": "regon_2",
            "krs": "krs_2",
        },
    ]
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_organization_retrieve(auth_client, organization):
    response = auth_client.get(
        f"/api/organizations/{organization['organization'][0].id}/"
    )
    expected_response = {
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
    }
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == expected_response


@pytest.mark.django_db
def test_organization_create(auth_client, organization, location):
    post_parameters = {
        "name": "name_1",
        "addresses": [
            {
                "location": location[0].id,
                "kind": organization["address_kind"][0].id,
                "zip_code": "zip",
                "address": "address",
            }
        ],
        "nip": "nip_1",
        "regon": "regon_1",
        "krs": "krs_1",
    }
    response = auth_client.post("/api/organizations/", post_parameters, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert remove_ids(response.data) == post_parameters


@pytest.mark.django_db
def test_organization_update(auth_client, organization, location):
    put_parameters = {
        "name": "new_name",
        "addresses": [
            {
                "location": location[0].id,
                "kind": organization["address_kind"][0].id,
                "zip_code": "zip",
                "address": "address",
            }
        ],
        "nip": "nip_2",
        "regon": "regon_2",
        "krs": "krs_2",
    }
    response = auth_client.put(
        f"/api/organizations/{organization['organization'][0].id}/",
        put_parameters,
        format="json",
    )
    organization = Organization.objects.get(name="new_name")
    assert organization.nip == "nip_2"
    assert response.status_code == status.HTTP_200_OK
    assert remove_ids(response.data) == put_parameters


@pytest.mark.django_db
def test_organization_delete(auth_client, organization):
    organization = Organization.objects.get(id=organization["organization"][0].id)
    response = auth_client.delete(f"/api/organizations/{organization.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Organization.DoesNotExist):
        organization.refresh_from_db()
