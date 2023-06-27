from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        ENG = ("eng", "English")
        KOR = ("kor", "Korean")

    class CurrencyChocies(models.TextChoices):
        CAD = ("cad", "Canadian Dollar")
        USD = ("usd", "United States Dollar")
        KRW = ("won", "Korean Won")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )

    last_name = models.CharField(
        max_length=150,
        editable=False,
    )

    name = models.CharField(
        max_length=150,
        default="",
    )

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )

    language = models.CharField(
        max_length=3,
        choices=LanguageChoices.choices,
    )

    currency = models.CharField(
        max_length=3,
        choices=CurrencyChocies.choices,
    )

    photo = models.ImageField(
        blank=True,
    )

    is_host = models.BooleanField(
        null=True,
    )
