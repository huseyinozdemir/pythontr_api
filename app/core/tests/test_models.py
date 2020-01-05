from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def test_user(email='test@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'email@hotmail.com'
        password = '123qwe'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'email@HOTMAIL.com'
        user = get_user_model().objects.create_user(email, 'qwe123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123qwe')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'email@hotmail.com',
            '123qwe'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_category_str(self):
        category = models.Category.objects.create(
            user=test_user(),
            name='Python programlama',
        )

        self.assertEqual(str(category), category.name)
