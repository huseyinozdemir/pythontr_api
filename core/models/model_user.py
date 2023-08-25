from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin

from django.conf import settings

from django.utils import timezone
from django.utils.text import slugify


def avatar_image_file_path(instance, filename):
    f_name, ext = filename.split('.')
    allowed_chars = \
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._"
    sanitized_filename = ''.join(c for c in f_name if c in allowed_chars)
    slug = slugify(sanitized_filename)
    file_path = f'{settings.AVATAR_ROOT}{instance.pk}/{slug}.{ext}'
    return file_path


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
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_slug(self):
        slug = slugify(self.username.replace('ı', 'i'))
        unique = slug
        number = 1

        while User.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        self.updated_at = timezone.now()
        self.slug = self.get_slug()

        return super(User, self).save(*args, **kwargs)

    @property
    def image_url(self):
        image_url = None
        if self.image:
            image_url = self.image.url.replace(settings.APLICATION_NAME, '')
        return image_url
