from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Services, Tag, Components

from services.serializers import ServiceSerializer, ServiceDetailSerializer


SERVICES_URL = reverse('services:services-list')

def detail_url(services_id):
    """ return services details Url """

    return reverse('services:services-details', args=[services_id])


def sample_tag(user, name='Service Tag'):
    """ Create and return simple tag  """
    return Tag.objects.create(user=user, name=name)

def sample_componenets(user, name='Service Components'):
    """  Create and return simple components """

    return Components.objects.create(user=user, name=name)


def sample_services(user, **params):
    """ create and return sample services """
    defaults = {
        'title' : 'Sample services',
        'price' : 5.00

    }
    defaults.update(params)

    return Services.objects.create(user=user, **defaults)

class PublicservicesApiTests(TestCase):
    """ Test unauthenticated services api """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that authentication is required """

        res = self.client.get(SERVICES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateservicesApiTests(TestCase):
    """  Test the authorized user """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpassword'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_services(self):
        """  Test Retrieving Tags """
        sample_services(user=self.user)
        sample_services(user=self.user)

        res = self.client.get(SERVICES_URL)

        services = Services.objects.all().order_by('-id')

        serializer = ServiceSerializer(services, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_services_limited_to_user(self):
        """ Test retrieving recipes for user """

        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'password123'
        )

        sample_services(user=user2)
        sample_services(user=self.user)

        res = self.client.get(SERVICES_URL)

        services = Services.objects.filter(user=self.user)
        serializer = ServiceSerializer(services, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_services_detail(self):
        """ Test Viewing a services details """
        services = sample_services(user=self.user)
        services.tags.add(sample_tag(user=self.user))
        services.components.add(sample_componenets(user=self.user))

        url = detail_url(services.id)
        res = self.client.get(url)

        serializer = ServiceDetailSerializer(services)
        self.assertEqual(res.data, serializer.data)


        
        
        

