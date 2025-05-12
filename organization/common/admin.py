from django.contrib import admin

from .models import AddressKind, Location, Currency, BankAccount

admin.site.register(AddressKind)
admin.site.register(Location)
admin.site.register(Currency)
admin.site.register(BankAccount)
