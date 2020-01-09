from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

from recipe.serializers import CategorySerializer


CATEGORIES_URL = reverse('recipe:category-list')


class PublicCategoryApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test1@hotmail.com',
            '123qwe1'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_categories(self):
        Category.objects.create(
            user=self.user, name='python programlama', short_name='python'
        )
        Category.objects.create(
            user=self.user, name='linux sistemleri', short_name='linux'
        )

        res = self.client.get(CATEGORIES_URL)

        categories = Category.objects.all().order_by('-name')
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_categories_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other1@hotmail.com',
            '123qwe'
        )
        Category.objects.create(user=user2, name='c# programlama',
                                short_name='c#')
        category = Category.objects.create(
            user=self.user, name="veritabani mysql", short_name='mysql'
        )

        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[1]['name'], category.name)
