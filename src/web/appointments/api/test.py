from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from web.appointments.models import Appointment
from web.users.models import User

class CustomAuthTokenTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_obtain_token_success(self):
        url = reverse('obtain_auth_token')
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_obtain_token_invalid_credentials(self):
        url = reverse('obtain_auth_token')
        data = {'username': self.username, 'password': 'wrongpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid credentials')


class AppointmentApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = User.objects.create_user(username='staff', password='password', is_staff=True)
        self.patient_user = User.objects.create_user(username='patient', password='password')
        self.appointment = Appointment.objects.create(doctor=self.staff_user, patient=self.patient_user, scheduled_at='2023-10-10T10:00:00Z')
        self.token = Token.objects.create(user=self.staff_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_appointment_list(self):
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_appointment_detail(self):
        url = reverse('appointment-detail', args=[self.appointment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.appointment.pk)

    def test_appointment_create(self):
        url = reverse('appointment-create')
        data = {
            'doctor': self.staff_user.id,
            'patient': self.patient_user.id,
            'scheduled_at': '2024-10-10T10:00:00Z'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_appointment_update(self):
        url = reverse('appointment-update', args=[self.appointment.pk])
        data = {'scheduled_at': '2024-11-11T11:00:00Z'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_appointment_destroy(self):
        url = reverse('appointment-destroy', args=[self.appointment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
