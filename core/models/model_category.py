from django.db import models

from django.conf import settings

from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, unique=True)
    title_h1 = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    short_name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    sort = models.SmallIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def get_slug(self):
        slug = slugify(self.name.replace('ı', 'i'))
        unique = slug
        number = 1

        while Category.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.title_h1:
            self.title_h1 = self.title

        self.slug = self.get_slug()

        return super(Category, self).save(*args, **kwargs)

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
