# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from base.models import AbstractBaseUser, BaseModel


class User(AbstractBaseUser):
    REQUIRED_VERIFY_FIELDS = [
        "is_verified_email"
    ]  # Add this to modify the which fields need to be verified for user authentication.
    REQUIRED_REGISTER_FIELDS = ["email", "phone"]

    # Profile
    username = models.CharField(max_length=100, null=True, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)

    is_block = models.BooleanField(default=False)

    image = models.TextField(null=True, blank=True)

    date_of_birth = models.DateField(null=True)

    # Phone
    phone = PhoneNumberField(blank=True, default="")

    # Email
    email = models.CharField(blank=True, default="", max_length=256)
    is_verified_email = models.BooleanField(default=False)
    verified_email_on = models.DateTimeField(null=True)
    email_verification_code = models.CharField(max_length=6, default=None, null=True)
    email_verification_expire_at = models.DateTimeField(null=True)

    # Role
    is_customer = models.BooleanField(default=False)

    # Reset password
    reset_password_email_key = models.CharField(max_length=6, null=True, blank=True)
    reset_password_emai_expire_at = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["email"], name="user_email_idx"),
        ]

    @property
    def is_verified(self):
        return all(
            [
                getattr(self, verify_field)
                for verify_field in self.REQUIRED_VERIFY_FIELDS
            ]
        )

    @property
    def is_registered(self):
        return all(
            [
                getattr(self, register_field) not in (None, "")
                for register_field in self.REQUIRED_REGISTER_FIELDS
            ]
        )
