from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    auction_end = models.DateTimeField()
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('smartphones', 'Smartphones'),
        ('fashion', 'Fashion'),
        ('home', 'Home'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default='other')
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('used', 'Used'),
        ('for_parts', 'For Parts'),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used')

    def __str__(self):
        return self.title

class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - {self.bid_amount} on {self.product.title}"

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
        ('buyer', 'Buyer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
    store_name = models.CharField(max_length=255, blank=True)
    store_logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    store_email = models.EmailField(blank=True)
    store_phone = models.CharField(max_length=20, blank=True)
    store_description = models.TextField(blank=True)
    payment_settings = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

class Payment(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Payment to {self.vendor.username} - {self.amount}"
