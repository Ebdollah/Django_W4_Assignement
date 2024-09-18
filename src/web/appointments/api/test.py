from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from web.appointments.models import Appointment
from web.users.models import User
from django.utils import timezone
from datetime import timedelta


class AppointmentTests(APITestCase):

    def setUp(self):
        # Create two users - one doctor and one patient
        self.doctor = User.objects.create_user(
            username='doctor1', password='password', is_staff=True)
        self.patient = User.objects.create_user(
            username='patient1', password='password')

        # Generate tokens for both users
        self.doctor_token = Token.objects.create(user=self.doctor)
        self.patient_token = Token.objects.create(user=self.patient)

        # Sample appointment data
        self.appointment_data = {
            'doctor': self.doctor.id,
            'patient': self.patient.id,
            'scheduled_at': timezone.now() + timedelta(days=1),
            'status': 'pending',
        }

        # Create an appointment to use in tests
        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now() + timedelta(days=2),
            status='pending'
        )

    def test_list_appointments(self):
        """
        Ensure a user (staff or non-staff) can view the list of appointments.
        """
        url = reverse('index')

        # Test for staff (doctor) access
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.doctor_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test for non-staff (patient) access
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.patient_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_appointment(self):
        """
        Ensure only staff users (doctor) can create an appointment.
        """
        url = reverse('create')

        # Test for staff (doctor) creation
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.doctor_token.key)
        response = self.client.post(url, self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test for non-staff (patient) creation
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.patient_token.key)
        response = self.client.post(url, self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_appointment(self):
        """
        Ensure a user (staff or non-staff) can retrieve an appointment.
        """
        url = reverse('detail', kwargs={'pk': self.appointment.pk})

        # Test for staff (doctor) access
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.doctor_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test for non-staff (patient) access
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.patient_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_appointment(self):
        """
        Ensure only staff users (doctor) can update an appointment.
        """
        url = reverse('update', kwargs={'pk': self.appointment.pk})
        updated_data = {'status': 'completed'}

        # Test for staff (doctor) update
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.doctor_token.key)
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

        # Test for non-staff (patient) update
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.patient_token.key)
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_appointment(self):
        """
        Ensure only staff users (doctor) can delete an appointment.
        """
        url = reverse('delete', kwargs={'pk': self.appointment.pk})

        # Test for staff (doctor) delete
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.doctor_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Test for non-staff (patient) delete
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.patient_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_report_appointments(self):
        """
        Ensure a doctor can view a report of their appointments.
        """
        url = reverse('report')

        # Test for doctor (staff) access
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.doctor_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test for non-staff (patient) access - should fail
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.patient_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_credentials(self):
        """
        Ensure invalid credentials return an error.
        """
        # Use invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_auth(self):
        """
        Test custom token authentication using CustomAuthToken view.
        """
        url = reverse('custom_login')
        response = self.client.post(
            url, {'username': 'doctor1', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
