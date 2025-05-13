from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from organization.utils import apply_user_context


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_modified_by",
        related_query_name="%(app_label)s_%(class)ss",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        apply_user_context(self)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class AddressKind(BaseModel):
    id = models.SlugField(max_length=20, primary_key=True)
    kind = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.kind}"


class Location(BaseModel):
    COUNTRY = "CR"
    REGION = "RG"
    CITY = "CT"

    KIND_CHOICES = [
        (COUNTRY, "Państwo"),
        (REGION, "Region"),
        (CITY, "Miasto"),
    ]
    name = models.CharField(max_length=255)
    parent_location = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children"
    )
    code = models.CharField(max_length=64, blank=True)
    location_kind = models.CharField(
        max_length=2, choices=KIND_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}"


class Currency(BaseModel):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.code})"


class BankAccount(BaseModel):
    number = models.CharField(
        max_length=255,
        unique=True,
        validators=[RegexValidator(regex=r"^\S+$", message="Spaces are not allowed.")],
    )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="bank_accounts",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    main_account = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.number}"
