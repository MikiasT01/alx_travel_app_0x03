from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

@shared_task
def send_booking_confirmation_email(booking_id, customer_email):
        subject = 'Booking Confirmation'
        message = f'Dear Customer,\n\nYour booking (ID: {booking_id}) has been confirmed. Thank you!\n\nBest,\nTravel App Team'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [customer_email]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print(f"Booking confirmation email sent to {customer_email} for booking {booking_id}")