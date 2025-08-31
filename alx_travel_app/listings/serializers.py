# alx_travel_app/listings/serializers.py
from rest_framework import serializers
from .models import Listing, Booking, Review

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['listing_id', 'title', 'description', 'price_per_night', 'location', 'capacity', 'created_at', 'updated_at']
        read_only_fields = ['listing_id', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['booking_id', 'listing', 'user_email', 'check_in_date', 'check_out_date', 'number_of_guests', 'total_price', 'created_at']
        read_only_fields = ['booking_id', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review_id', 'listing', 'user_email', 'rating', 'comment', 'created_at']
        read_only_fields = ['review_id', 'created_at']