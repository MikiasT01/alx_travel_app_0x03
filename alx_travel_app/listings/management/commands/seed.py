# alx_travel_app/listings/management/commands/seed.py
from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review
from django.utils import timezone
import uuid

class Command(BaseCommand):
    help = 'Seeds the database with sample listings, bookings, and reviews'

    def handle(self, *args, **options):
        # Create sample listings
        listings_data = [
            {
                'title': 'Cozy Mountain Cabin',
                'description': 'A peaceful retreat in the mountains.',
                'price_per_night': 150.00,
                'location': 'Alps, Switzerland',
                'capacity': 4
            },
            {
                'title': 'Beachfront Villa',
                'description': 'Luxury villa with ocean views.',
                'price_per_night': 300.00,
                'location': 'Maldives',
                'capacity': 6
            }
        ]
        for data in listings_data:
            Listing.objects.create(**data)

        # Create sample bookings
        listings = Listing.objects.all()
        bookings_data = [
            {
                'listing': listings[0],
                'user_email': 'john.doe@example.com',
                'check_in_date': timezone.now().date() + timezone.timedelta(days=1),
                'check_out_date': timezone.now().date() + timezone.timedelta(days=5),
                'number_of_guests': 2,
                'total_price': 750.00
            },
            {
                'listing': listings[1],
                'user_email': 'jane.smith@example.com',
                'check_in_date': timezone.now().date() + timezone.timedelta(days=10),
                'check_out_date': timezone.now().date() + timezone.timedelta(days=15),
                'number_of_guests': 4,
                'total_price': 1500.00
            }
        ]
        for data in bookings_data:
            Booking.objects.create(**data)

        # Create sample reviews
        reviews_data = [
            {
                'listing': listings[0],
                'user_email': 'john.doe@example.com',
                'rating': 4,
                'comment': 'Great place, very cozy!'
            },
            {
                'listing': listings[1],
                'user_email': 'jane.smith@example.com',
                'rating': 5,
                'comment': 'Amazing view and service!'
            }
        ]
        for data in reviews_data:
            Review.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with sample data'))