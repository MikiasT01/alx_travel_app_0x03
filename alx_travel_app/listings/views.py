import requests
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Payment, Booking
from django.core.mail import send_mail
from celery import shared_task
from .tasks import send_booking_confirmation_email

@shared_task
def send_payment_confirmation_email(booking_id, email):
        booking = Booking.objects.get(id=booking_id)
        subject = 'Payment Confirmation'
        message = f'Thank you for your booking {booking.id}. Payment of ${booking.payment.amount} has been confirmed.'
        send_mail(subject, message, 'from@example.com', [email])
        return True

@api_view(['POST'])
def initiate_payment(request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            amount = booking.total_amount  # Assume this field exists
            data = {
                'amount': str(amount),
                'currency': 'ETB',
                'email': request.user.email,  # Assume authenticated user
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'tx_ref': f"tx_{booking_id}_{booking.created_at.timestamp()}",
                'callback_url': 'http://localhost:8000/api/verify-payment/',
                'return_url': 'http://localhost:8000/payment-success/',
                'customization[title]': 'Travel Booking Payment'
            }
            headers = {
                'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            response = requests.post('https://api.chapa.co/v1/transaction/initialize', json=data, headers=headers)
            result = response.json()
            if response.status_code == 200 and result.get('status') == 'success':
                payment = Payment.objects.create(
                    booking=booking,
                    transaction_id=result['data']['reference'],
                    amount=amount,
                    status='Pending'
                )
                return Response({'checkout_url': result['data']['checkout_url'], 'transaction_id': payment.transaction_id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': result.get('message', 'Payment initiation failed')}, status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def verify_payment(request, transaction_id):
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            headers = {
                'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'
            }
            response = requests.get(f'https://api.chapa.co/v1/transaction/verify/{transaction_id}', headers=headers)
            result = response.json()
            if response.status_code == 200 and result.get('status') == 'success':
                payment.status = 'Completed'
                payment.save()
                send_payment_confirmation_email.delay(payment.booking.id, payment.booking.user.email)  # Assume user relation
                return Response({'status': 'Completed', 'message': 'Payment verified and email sent'}, status=status.HTTP_200_OK)
            else:
                payment.status = 'Failed'
                payment.save()
                return Response({'status': 'Failed', 'message': result.get('message', 'Verification failed')}, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_booking(request):
        # Existing booking creation logic
        booking = Booking.objects.create(user=request.user, total_amount=100.00)  # Example
        # Trigger booking confirmation email
        send_booking_confirmation_email.delay(booking.id)
        response = initiate_payment(request, booking.id)
        if response.status_code == 200:
            return Response({'booking_id': booking.id, 'payment_url': response.data['checkout_url']}, status=status.HTTP_201_CREATED)
        return response