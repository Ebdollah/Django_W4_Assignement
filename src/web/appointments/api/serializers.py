from rest_framework import serializers
from web.appointments.models import Appointment
from django.utils import timezone


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate_scheduled_at(self, value):
        # Ensure the scheduled time is in the future
        if value < timezone.now():
            raise serializers.ValidationError("The appointment time must be in the future.")
        return value

    def validate(self, data):
        doctor = data.get('doctor')
        scheduled_at = data.get('scheduled_at')

        # Check if the doctor already has an appointment at the scheduled time
        if Appointment.objects.filter(doctor=doctor, scheduled_at=scheduled_at).exists():
            raise serializers.ValidationError("This doctor already has an appointment at the scheduled time.")

        return data
