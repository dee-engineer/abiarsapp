from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random
import string
from .manager import UserManager

def generate_unique_tax_id():
    unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return unique_id


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    objects = UserManager()
    username = models.CharField(max_length=200, unique=True, blank=True, null=True)
    USERNAME_FIELD = 'tax_id'

    tax_id = models.CharField(max_length=8, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    def get_full_name(self) -> str:
        return super().get_full_name()

@receiver(pre_save, sender=User)
def generate_user_tax_id(sender, instance, **kwargs):
    if not instance.tax_id:
        instance.tax_id = generate_unique_tax_id()

