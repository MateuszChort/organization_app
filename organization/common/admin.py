from django.contrib import admin

from .models import AddressKind, BankAccount, Currency, Location

admin.site.register(AddressKind)
admin.site.register(Location)
admin.site.register(Currency)
admin.site.register(BankAccount)
