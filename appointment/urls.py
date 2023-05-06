from django.urls import path
from . import views

urlpatterns = [
    path('appointment/', views.home, name='home'),
    path('appointment/hello/', views.get_calender_event, name='hello'),
    path('appointment/token/', views.google_calendar_permission, name='doctor_list'),
    path('appointment/google_calendar_callback/', views.google_calendar_callback, name='google_calendar_callback'),
    path('appointment/success_page/', views.success, name='success_page'),

    # for appointment
    path('appointment/list/', views.appointment_list, name='appointment_list'),
    path('appointment/<int:doctor_id>/book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointment/details/<int:doctor_id>/appointments/<str:appointment_id>/', views.appointment_details, name='appointment_details'),
    
]