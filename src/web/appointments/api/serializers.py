from rest_framework import serializers
from web.appointments.models import Appointment
from web.users.models import User
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Provides a simple representation of user details, including
    'id' and 'name'.
    """
    class Meta:
        model = User
        fields = ['id', 'name']


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Appointment model.
    Includes nested UserSerializer for both the doctor and the patient.
    Serializes all fields of the Appointment model and provides
    custom validation for scheduling constraints.
    """
    doctor = UserSerializer()  # Use nested serializer for doctor
    patient = UserSerializer()  # Use nested serializer for patient

    class Meta:
        model = Appointment
        fields = '__all__'

    def validate_scheduled_at(self, value):
        """
        Validates that the 'scheduled_at' field represents a future date and time.

        Raises:
            serializers.ValidationError: If the scheduled time is in the past.
        """
        if value < timezone.now():
            raise serializers.ValidationError(
                "The appointment time must be in the future.")
        return value

    def validate(self, data):
        """
        Validates the entire Appointment object.
        Ensures that a doctor does not have two appointments at the same time.

        Args:
            data: The validated appointment data.

        Raises:
            serializers.ValidationError: If a doctor already has an appointment
            at the same 'scheduled_at' time.

        Returns:
            dict: The validated appointment data.
        """
        doctor = data.get('doctor')
        scheduled_at = data.get('scheduled_at')

        # Check if the doctor already has an appointment at the scheduled time
        if Appointment.objects.filter(doctor=doctor, scheduled_at=scheduled_at).exists():
            raise serializers.ValidationError(
                "This doctor already has an appointment at the scheduled time.")

        return data
