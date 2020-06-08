from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Service, Tag, Components

from service.serializers import ServiceSerializer, ServiceDetailSerializer


SERVICES_URL = reverse('service:services-list')

def detail_url(services_id):
    """ return services details Url """

    return reverse('service:services-details', args=[services_id])


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

    return Service.objects.create(user=user, **defaults)

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

        services = Service.objects.all().order_by('-id')

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

        services = Service.objects.filter(user=self.user)
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

    def test_create_basic_services(self):
        """ Test Create Service """

        payload = {
            'title' : 'Fitting Job',
            'price' : 100.00
        }

        res = self.client.post(SERVICES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        services = Service.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(services, key))
    
    def test_create_services_with_tag(self):
        """  Test creating a services with tag """
        tag1 = sample_tag(user=self.user, name='Electrical')
        tag2 = sample_tag(user=self.user, name='Distribution')

        payload = {
            'title' : 'Fitting Job',
            'tags' : [tag1.id, tag2.id],
            'price' : 100.00
        }

        res = self.client.post(SERVICES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        services = Service.objects.get(id=res.data['id'])
        tags = services.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_services_with_components(self):
        """ Test Creating services with components"""

        component1 = sample_componenets(user=self.user, name='switch')
        component2 = sample_componenets(user=self.user, name='switchboard')

        payload = {
            'title' : 'Fitting Job',
            'components' : [component1.id, component2.id],
            'price' : 100.00
        }

        res =self.client.post(SERVICES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        services = Service.objects.get(id=res.data['id'])
        components = Service.components.all()
        self.assertEqual(components.count(), 2)
        self.assertIn(component1, components)
        self.assertIn(component2, components)

    def test_partial_update_services(self):
        """  Test updating a service with patch """

        services = sample_services(user=self.user)
        services.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Transformer')

        payload = {'title' : 'sample service job' , 'tags' : [new_tag.id]}
        url = detail_url(services.id)
        self.client.patch(url, payload)

        services.refresh_from_db()

        self.assertEqual(services.title, payload['title'])
        tags = services.tags.all()

        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_services(self):
        """ Test updating the services """

        services = sample_services(user=self.user)
        services.tags.add(sample_tag(user=self.user))
        payload = {
            'title' : 'Sample services',
            'price' : 5.00
        }
        url = detail_url(services.id)
        self.client.put(url, payload)

        services.refresh_from_db()
        self.assertEqual(services.title, payload['title'])
        self.assertEqual(services.price, payload['price'])
        tags = services.tags.all()
        self.assertEqual(len(tags), 0)
        











        






        
        
        

