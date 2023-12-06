from django.utils.translation import gettext as _
from django.contrib.auth.models import BaseUserManager

    


class UserManager(BaseUserManager):

    def create_user(self, tax_id, password, **extra_fields):
        if not tax_id:
            raise ValueError(_('Users must have a tax ID'))

        user = self.model(tax_id=tax_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, tax_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(tax_id, password, **extra_fields)
