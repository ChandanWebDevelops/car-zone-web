from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:category_detail", args=[self.slug])

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    country_of_origin = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Car(models.Model):
    # Choices for Transmission and Fuel Type
    class TRANSMISSION_CHOICES(models.TextChoices):
        AUTOMATIC = 'a', 'Automatic'
        MANUAL = 'm', 'Manual'
        CVT = 'c', 'CVT'

    class FUEL_CHOICES(models.TextChoices):
        GAS = 'g', 'Gasoline'
        DIESEL = 'd', 'Diesel'
        ELECTRIC = 'e', 'Electric'
        HYBRID = 'h', 'Hybrid'

    # RelationShip

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cars')
    
    # Core Details
    model_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, db_index=True)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Specifications
    mileage = models.PositiveIntegerField(help_text="Mileage in miles or km")
    transmission = models.CharField(max_length=2, choices=TRANSMISSION_CHOICES, default=TRANSMISSION_CHOICES.AUTOMATIC)
    fuel_type = models.CharField(max_length=2, choices=FUEL_CHOICES, default=FUEL_CHOICES.GAS)
    color = models.CharField(max_length=50, blank=True)

    # Description & Media
    description = models.TextField()
    image = models.ImageField(upload_to='cars/%Y/%m/%d', blank=True)

    # Inventory & Status
    stock = models.PositiveIntegerField(default=1)
    # For specific cars, but > 1 for general models
    is_available = models.BooleanField(default=True)

    # TimeStamps
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Newest cars first
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return f"{self.year} {self.brand.name} {self.model_name}"

    def get_absolute_url(self):
        return reverse("store:car_detail", args=[self.id, self.slug])
    
class Order(models.Model):
    # Linking to User (Optional, for guest checkout)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Another field 
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Order {self.id} - {self.first_name} {self.last_name}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity