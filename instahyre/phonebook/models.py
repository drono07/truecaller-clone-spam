from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, mobile, password=None, **extra_fields):

        if not email:
            email = None

        user = self.model(
            email=self.normalize_email(email),
            mobile=mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, mobile, password, **extra_fields)


class MyUser(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email', 'full_name']

    objects = MyUserManager()
    
    def __str__(self):
        return f"User : {self.full_name} & Mobile : {self.mobile}"
    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return True
    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return True 

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set_phonebook',
        blank=True,
        help_text='Permissions --> user.',
        verbose_name='user_level_permissions',
    )

class PhoneEntry(models.Model):
    name = models.CharField(max_length=255, default="unknown")
    number = models.CharField(max_length=15)
    spam_score = models.IntegerField(default=0)
    is_spam = models.BooleanField(default=False)
    marked_by = models.ManyToManyField(MyUser, through='SpamReport', related_name='marked_spam')

    def __str__(self):
        return self.number

class SpamReport(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    phone_entry = models.ForeignKey(PhoneEntry, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactList(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact_name} ({self.contact_number})"