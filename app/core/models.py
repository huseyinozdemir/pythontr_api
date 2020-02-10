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


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager,
                     self).get_queryset().filter(is_active=True,
                                                 is_delete=False)


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


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    sort = models.SmallIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    @property
    def full_category_name(self):
        return self.__str__()

    def __unicode__(self):
        return self.name

    def __str__(self):
        full_path = [self.name]
        k = self.parent_category
        while k is not None:
            full_path.append(k.name)
            k = k.parent_category

        full_path = ' / '.join(full_path[::-1])

        return full_path


class Article(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        Category,
        related_name='article',
    )
    title = models.CharField(max_length=255, unique=True)
    title_h1 = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    read_count = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_active = models.BooleanField(default=False)
    is_approval = models.BooleanField(default=False)
    approval_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='approval_user',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_delete = models.BooleanField(default=False)

    objects = ArticleManager()

    def __str__(self):
        return self.title
