from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, null=False)
    # phone_regex = RegexValidator(
    #     regex=r'^\+?1?\d{10,11}$',
    #     message="شماره تلفن باید عدد و بین 10 تا 11 رقم باشد.")
    phone_number = models.CharField(max_length=100, unique=True, null=False)
    validation = models.BooleanField(default=False)
    account_creation_date = models.DateTimeField(
        'date published', default=timezone.now)
    # email_regex = RegexValidator(
    #     regex=r"[^@]+@[^@]+\.[^@]+", message="فرمت ایمیل اشتباه است.")
    email = models.CharField(max_length=70, null=False, unique=True)
    car = models.CharField(max_length=10, null=True, blank=True)
    plaque = models.CharField(max_length=5, null=True, blank=True)
