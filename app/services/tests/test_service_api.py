from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from services.serializers import TagSerializers


TAG_URLS = reverse('services:tag-list')

class PublicTagsAPITests(TestCase):
    """ Test this publicly avaliable API """

    def setup(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test the login is required for retrieving api """

        res = self.client.get(TAG_URLS)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    """  Test the authorized user """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """  Test Retrieving Tags """
        Tag.objects.create(user=self.user, name='Electrical')
        Tag.objects.create(user=self.user, name='Transformer')

        res= self.client.get(TAG_URLS)

        tags = Tag.objects.all().order_by('-name')

        serializer = TagSerializers(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_tags_limited_to_user(self):
        """  Test thetags that are not authenticated user """

        user2 = get_user_model().objects.create_user(

            'other@test.com',
            'testpassword'
        )
        Tag.objects.create(user=user2, name='Mech')
        tag = Tag.objects.create(user=self.user, name='Mechanical')

        res = self.client.get(TAG_URLS)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successfull(self):
        """ Test Creating a New tag """

        payload = {'name': 'Test tag'}

        self.client.post(TAG_URLS, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']

        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """ Test Creating a new tag with invalid payload """

        payload = {'name' : ''}
        res = self.client.post(TAG_URLS, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        






















    



