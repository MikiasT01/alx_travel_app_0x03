# alx_travel_app_0x02

## Payment Integration with Chapa API

This project integrates the Chapa Payment Gateway into a Django-based travel booking application.

### Setup
- Duplicate from `alx_travel_app_0x01`.
- Install dependencies: `pip3 install djangorestframework requests celery redis python-dotenv`.
- Configure `.env` with `CHAPA_SECRET_KEY`.
- Run migrations: `python3 manage.py migrate`.
- Start Redis and Celery: `redis-server` and `celery -A alx_travel_app worker --loglevel=info`.

### Endpoints
- `POST /api/create-booking/`: Initiate a booking with payment.
- `POST /api/initiate-payment/<booking_id>/`: Start payment process.
- `GET /api/verify-payment/<transaction_id>/`: Verify payment status.

### Testing
- Use Chapa sandbox for testing.
- Screenshots included for payment initiation, verification, and status update.