from django.urls import path
from .views import *

urlpatterns = [
    path('appointments/', AppointmentListApiView.as_view(), name='index'),
    path('login/', CustomAuthToken.as_view(), name='custom_login'),
    path('appointments/<int:pk>/',
         AppointmentDetailApiView.as_view(), name='detail'),

    path('appointments/create/', AppointmentCreateApiView.as_view(), name='create'),

    path('appointments/update/<int:pk>/',
         AppointmentUpdateAPIView.as_view(), name='update'),

    path('appointments/delete/<int:pk>/',
         AppointmentDestroyAPIView.as_view(), name='delete'),

    path('appointments/report-appointments/',
         AppointmentReportApiView.as_view(), name='report')
]
