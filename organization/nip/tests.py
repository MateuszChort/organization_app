# pylint: disable=unused-argument
import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_nip(auth_client, nip_search_mock):
    response = auth_client.get("/api/nip/5/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [{"NIP": "123456"}]


@pytest.mark.django_db
def test_get_nip_not_int(auth_client, nip_search_mock):
    response = auth_client.get("/api/nip/aa/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_nip_404(auth_client, nip_search_mock_404):
    response = auth_client.get("/api/nip/555/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == [
        {
            "ErrorCode": "4",
        }
    ]
