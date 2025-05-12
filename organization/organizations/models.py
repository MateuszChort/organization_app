from django.db import models

from organization.common.models import BaseModel


class Address(BaseModel):
    location = models.ForeignKey("common.Location", on_delete=models.CASCADE)
    kind = models.ForeignKey("common.AddressKind", on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.address}, {self.zip_code}"


class Organization(models.Model):
    name = models.CharField(max_length=255)
    addresses = models.ManyToManyField("organizations.Address")
    nip = models.CharField(max_length=10)
    regon = models.CharField(max_length=14)
    krs = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def main_account(self):
        bank_account = self.bank_accounts.filter(main_account=True)
        return bank_account[0] if bank_account.exists() else None
