from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import AddressKind, BankAccount, Currency, Location


class AddressKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressKind
        fields = ["id", "kind"]


class LocationSerializer(serializers.ModelSerializer):
    parent_location = RecursiveField(allow_null=True)

    class Meta:
        model = Location
        fields = ["id", "name", "parent_location", "code", "location_kind"]


class LocationCreateUpdateSerializer(WritableNestedModelSerializer):
    parent_location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), allow_null=True
    )

    def validate(self, attrs):
        if (
            (parent_location := attrs.get("parent_location"))
            and self.instance
            and parent_location.id == self.instance.id
        ):
            raise serializers.ValidationError(
                "Parent location cannot reference to the same object"
            )
        return attrs

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "code",
            "location_kind",
            "parent_location",
        ]


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["code", "name"]


class BankAccountCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ["number", "currency", "organization", "is_active", "main_account"]


class BankAccountSerializer(BankAccountCreateUpdateSerializer):
    from organization.organizations.serializers import OrganizationSerializer

    organization = OrganizationSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)

    class Meta(BankAccountCreateUpdateSerializer.Meta):
        pass
