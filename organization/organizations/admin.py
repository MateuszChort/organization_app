from django.contrib import admin

from .models import Address, Organization

admin.site.register(Address)
admin.site.register(Organization)
