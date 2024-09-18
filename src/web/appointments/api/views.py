from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, status, mixins, permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend

from web.appointments.models import Appointment
from web.appointments.api.serializers import AppointmentSerializer
from web.appointments.api.permissions import IsStaffOrReadOnly, AllowAny
from web.appointments.api.pagination import CustomPagination
from django.shortcuts import render, get_object_or_404

from web.users.models import User


class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication endpoint that issues a token after verifying
    the provided username and password. If credentials are valid, a token is returned;
    otherwise, an error response is sent.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for custom token authentication.
        Requires 'username' and 'password' in the request body.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class AppointmentListApiView(generics.ListAPIView):
    """
    View to list all appointments. 
    Allows filtering by doctor, patient, and scheduled_at fields. 
    Accessible by both staff and non-staff, but non-staff users have read-only access.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'patient', 'scheduled_at']
    pagination_class = CustomPagination


class AppointmentDetailApiView(generics.RetrieveAPIView):
    """
    View to retrieve a single appointment by its primary key (ID).
    Accessible by both staff and non-staff users, but non-staff users have read-only access.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    lookup_field = 'pk'
    permission_classes = [IsStaffOrReadOnly]


class AppointmentCreateApiView(generics.CreateAPIView):
    """
    View to create a new appointment.
    Only accessible by staff users for creating new appointment records.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsStaffOrReadOnly]


class AppointmentUpdateAPIView(generics.UpdateAPIView):
    """
    View to update an existing appointment by its primary key (ID).
    Supports partial updates. Accessible only by staff users.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    lookup_field = 'pk'
    permission_classes = [IsStaffOrReadOnly]

    def partial_update(self, request, *args, **kwargs):
        """
        Handles partial updates for appointments.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        """
        Performs the update after validation.
        This is where additional logic during the update process can be added.
        """
        serializer.save()


class AppointmentDestroyAPIView(generics.DestroyAPIView):
    """
    View to delete an existing appointment by its primary key (ID).
    Only accessible by staff users.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    lookup_field = 'pk'
    permission_classes = [IsStaffOrReadOnly]

    def perform_destroy(self, instance):
        """
        Performs the deletion of the appointment instance.
        Handles errors if the appointment doesn't exist.
        """
        try:
            super().perform_destroy(instance)
            return Response({'message': 'Appointment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
