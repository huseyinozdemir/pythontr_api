from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Slider


SLIDERS_URL = reverse('recipe:slider-list')
SLIDERS_URL_ME = '{}{}'.format(SLIDERS_URL, '?me=true')


def detail_url(id=1):
    return reverse('recipe:slider-detail', args=[id])


class PublicSliderApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                'test1@hotmail.com',
                '123qwe'
        )
        self.client = APIClient()
        # self.client.force_authenticate(self.user)

    def test_list_not_login_requried(self):
        res = self.client.get(SLIDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_404_slider_login_not_required(self):
        url = detail_url(1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)

    def test_dont_create_slider(self):
        # self.client.force_authenticate(self.user)
        content = {
            'title': 'How to update for dictionary',
            'description': 'Bla bla bla',
            'link': 'https:/www.pythontr.com',
            'user': [self.user.id]
        }
        res = self.client.post(SLIDERS_URL, content)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_slider(self):
        slider = Slider.objects.create(
            title='How to update for dictionary',
            description='Bla bla bla',
            link='https:/www.pythontr.com',
            is_active=True
        )
        url = detail_url(slider.id)

        res = self.client.get(url)
        self.assertEquals(res.status_code, status.HTTP_200_OK)


class PrivateSliderApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                'test12@hotmail.com',
                '123qwe'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_slider(self):
        self.is_staff = True
        content = {
            'title': 'How to update for dictionary',
            'description': 'Bla bla bla',
            'link': 'https:/www.pythontr.com',
            'user': [self.user.id]
        }

        res = self.client.post(SLIDERS_URL, content)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_update_slider(self):
        self.is_staff = True

        slider = Slider.objects.create(
            title='How to update for dictionary',
            description='Bla bla bla',
            link='https:/www.pythontr.com',
            is_active=True,
            user=self.user
        )
        content = {
            'id': slider.id,
            'title': 'Deneme',
            'description': 'Bla bla bla',
            'link': 'https:/www.pythontr.com',
            'user': [self.user.id]
        }
        url = detail_url(slider.id)

        res = self.client.put(url, content)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data['title'], content['title'])

    def test_dont_delete_slider(self):
        self.is_staff = True
        slider = Slider.objects.create(
            title='How to update for dictionary',
            description='Bla bla bla',
            link='https:/www.pythontr.com',
            is_active=True,
            user=self.user
        )
        url = detail_url(slider.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_filter_me_get(self):
        self.is_staff = True

        different_user = get_user_model().objects.create_user(
                'differentuser@hotmail.com',
                '123qwe'
        )

        Slider.objects.create(
            title='How to update for dictionary',
            description='Bla bla bla',
            link='https:/www.pythontr.com',
            is_active=True,
            user=self.user
        )

        Slider.objects.create(
            title='Python for and wihle syntax',
            description='Bla bla bla',
            link='https:/www.pythontr.com',
            is_active=True,
            user=different_user
        )
        Slider.objects.create(
            title='Mongoos and Nodejs',
            description='Bla bla bla',
            link='https:/www.pythontr.com',
            is_active=True,
            user=self.user
        )
        res = self.client.get(SLIDERS_URL_ME)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
