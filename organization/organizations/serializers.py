from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from organization.common.serializers import LocationSerializer

from .models import Address, Organization


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "location", "kind", "zip_code", "address"]


class AddressSerializer(AddressCreateSerializer):
    location = LocationSerializer()

    class Meta(AddressCreateSerializer.Meta):
        pass


class OrganizationCreateSerializer(WritableNestedModelSerializer):
    addresses = AddressCreateSerializer(many=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "addresses", "nip", "regon", "krs"]


class OrganizationSerializer(OrganizationCreateSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta(OrganizationCreateSerializer.Meta):
        pass
