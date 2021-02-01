# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, is_staff=False, is_active=True, **extra_fields):
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    """Custom User model with email field as username."""
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=40)
    last_name = models.CharField(_('last name'), max_length=40)

    is_staff = models.BooleanField(_('is staff'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('-created', '-modified', )

    def clean(self):
        super().clean()

        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.email
