from django.db import models

from django.conf import settings


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
