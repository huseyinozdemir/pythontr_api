from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core.models import Slider


def test_user(email='testarticle@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


def test_user_other(email='testarticleother@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_slider_str(self):
        user = test_user_other()
        slider = Slider.objects.create(
            user=user,
            title='Python programlama',
            description='python',
            link='https://www.pythontr.com',
            approval_user=user,
        )

        self.assertEqual(str(slider), slider.title)

    def test_slider_title_uniqe_check(self):
        Slider.objects.create(
            user=test_user(),
            title='Python programlama',
            description='python',
            link='https://www.pythontr.com',
            approval_user=test_user_other(),
        )
        with self.assertRaises(IntegrityError):
            Slider.objects.create(
                user=test_user(),
                title='Python programlama',
                description='python',
                link='https://www.pythontr.com',
                approval_user=test_user_other(),
            )
