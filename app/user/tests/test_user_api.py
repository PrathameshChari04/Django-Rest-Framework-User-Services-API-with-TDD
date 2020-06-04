from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objections.create_user(**params)

class PublicUserAPITests(TestCase):
    """ Test this API Publicly """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test Creating user with valid is successfull """

        payload = {

            'email' : 'test@gmail.com',
            'password' : 'Testpass',
            'name' : 'Test name'



        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)


    def test_user_exists(self):
        """ Checking user exits """
        payload = {'email' : 'test@gmail.com', 'password': 'Testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_pass_to_short(self):

        payload = {'email' : 'test@gmail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(

            email= payload['email']

        ).exists()

        self.assertFalse(user_exists)





     

