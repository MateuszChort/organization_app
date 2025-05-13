from django_filters import rest_framework as filters

from organization.common.models import Location
from organization.filters import NumberInFilter


class OrganizationFilters(filters.FilterSet):
    addresses_location = NumberInFilter(method="location_filter")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    addresses_location_string = filters.CharFilter(
        field_name="addresses__location__name", lookup_expr="icontains"
    )
    nip = filters.CharFilter(field_name="nip", lookup_expr="icontains")
    regon = filters.CharFilter(field_name="regon", lookup_expr="icontains")

    def location_filter(self, queryset, name, value):
        locations = Location.get_children_from_multiple_locations(value)
        return queryset.filter(
            addresses__location__id__in=locations.values_list("id", flat=True)
        )
