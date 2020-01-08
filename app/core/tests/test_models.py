from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core import models


def test_user(email='test@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


def test_user_other(email='test2@hotmail.com', password='123qwe'):
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
            short_name='python',
        )

        self.assertEqual(str(category), category.name)

    def test_catgory_name_uniqe_check(self):
        models.Category.objects.create(
            user=test_user(),
            name='Python',
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
