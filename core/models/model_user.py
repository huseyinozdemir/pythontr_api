import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin

from django.conf import settings


def avatar_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join(settings.AVATAR_ROOT, filename)


def validate_user(**kwargs):
    for key, value in kwargs.items():
        if not value:
            raise ValueError('Users must have an {} address'.format(value))


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        validate_user(email=email)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, upload_to=avatar_image_file_path,
                              blank=True)
    about_me = models.TextField(blank=True)
    linkedin = models.CharField(max_length=255, blank=True)
    is_notification_email = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_ban = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def image_url(self):
        image_url = None
        if self.image:
            image_url = self.image.url.replace(settings.APLICATION_NAME, '')
        return image_url
