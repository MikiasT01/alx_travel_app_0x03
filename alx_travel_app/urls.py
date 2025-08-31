from django.urls import path
from listings import views

urlpatterns = [
    path('api/create-booking/', views.create_booking, name='create_booking'),
    path('api/initiate-payment/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('api/verify-payment/<str:transaction_id>/', views.verify_payment, name='verify_payment'),
]