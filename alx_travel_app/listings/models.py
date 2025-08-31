# Create your models here.
# alx_travel_app/listings/models.py
from django.db import models
import uuid

class Listing(models.Model):
    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    capacity = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['location'], name='location_idx')]

    def __str__(self):
        return self.title

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user_email = models.EmailField(null=False, blank=False)
    check_in_date = models.DateField(null=False)
    check_out_date = models.DateField(null=False)
    number_of_guests = models.PositiveIntegerField(null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(check_in_date__lt=models.F('check_out_date')), name='check_in_before_check_out')
        ]
        indexes = [models.Index(fields=['listing', 'check_in_date'], name='booking_listing_date_idx')]

    def __str__(self):
        return f"Booking {self.booking_id} for {self.listing.title}"

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user_email = models.EmailField(null=False, blank=False)
    rating = models.PositiveSmallIntegerField(null=False, validators=[models.MinValueValidator(1), models.MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['listing', 'created_at'], name='review_listing_date_idx')]

    def __str__(self):
        return f"Review {self.review_id} for {self.listing.title}"
    


class Payment(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for Booking {self.booking.id}"