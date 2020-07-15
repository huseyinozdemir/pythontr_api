from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core import models


def test_user(email='test@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


def test_user_other(email='test2@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_category_str(self):
        category = models.Category.objects.create(
            user=test_user(),
            name='Python programlama',
            short_name='python',
        )

        self.assertEqual(str(category), category.name)

    def test_catgory_name_uniqe_check(self):
        models.Category.objects.create(
            user=test_user(),
            name='PythonTest',
            short_name='python',
        )
        with self.assertRaises(IntegrityError):
            models.Category.objects.create(
                user=test_user_other(),
                name='Python',
                short_name='python2',
            )

    def test_catgory_short_name_uniqe_check(self):
        models.Category.objects.create(
            user=test_user(),
            name='Python2',
            short_name='python',
        )
        with self.assertRaises(IntegrityError):
            models.Category.objects.create(
                user=test_user_other(),
                name='Python',
                short_name='python',
            )
