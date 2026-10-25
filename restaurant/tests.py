from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, Menu
from .serializers import MenuSerializer


class MenuModelAndSerializerTests(TestCase):
    def test_menu_model_and_serializer(self):
        item = Menu.objects.create(title='Greek Salad', price=Decimal('12.50'), inventory=10)
        data = MenuSerializer(item).data
        self.assertEqual(data['title'], 'Greek Salad')
        self.assertEqual(data['price'], '12.50')
        self.assertEqual(str(item), 'Greek Salad')

    def test_negative_price_is_invalid(self):
        serializer = MenuSerializer(data={'title': 'Invalid', 'price': '-1', 'inventory': 1})
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)


class MenuAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='chef', password='strong-pass-123')
        Menu.objects.create(title='Bruschetta', price='8.50', inventory=20)

    def test_get_menu_is_public(self):
        response = self.client.get('/restaurant/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Bruschetta')

    def test_post_menu_requires_authentication(self):
        response = self.client.post('/restaurant/menu/', {'title': 'Pasta', 'price': '14.00', 'inventory': 5})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_post_menu(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/restaurant/menu/', {'title': 'Pasta', 'price': '14.00', 'inventory': 5})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)


class BookingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='guest', password='strong-pass-123')
        self.payload = {
            'name': 'Alex',
            'no_of_guests': 2,
            'booking_date': (timezone.now() + timedelta(days=1)).isoformat(),
        }

    def test_booking_get_and_post_require_authentication(self):
        response = self.client.get('/restaurant/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(self.user)
        response = self.client.post('/restaurant/bookings/', self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], 'guest')

    def test_booking_list_contains_only_current_users_bookings(self):
        Booking.objects.create(user=self.user, **self.payload)
        other = User.objects.create_user(username='other', password='strong-pass-123')
        Booking.objects.create(user=other, **self.payload)
        self.client.force_authenticate(self.user)
        response = self.client.get('/restaurant/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_missing_booking_field_is_invalid(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/restaurant/bookings/', {'name': 'Alex'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('no_of_guests', response.data)


class AuthenticationTests(APITestCase):
    def test_registration_login_and_logout(self):
        response = self.client.post('/restaurant/auth/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'strong-pass-123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/restaurant/auth/login/', {
            'username': 'newuser',
            'password': 'strong-pass-123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")
        response = self.client.post('/restaurant/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
