import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Brand, Car

print("Clearing old data...")
Car.objects.all().delete()
Brand.objects.all().delete()
Category.objects.all().delete()

print("Creating Categories...")
sedan = Category.objects.create(name='Sedan', slug='sedan', description='Comfortable and fuel-efficient cars.')
suv = Category.objects.create(name='SUV', slug='suv', description='Sport Utility Vehicles for families and off-roading.')
truck = Category.objects.create(name='Truck', slug='truck', description='Heavy-duty pickup trucks.')
electric = Category.objects.create(name='Electric', slug='electric', description='Zero-emission electric vehicles.')
sports = Category.objects.create(name='Sports', slug='sports', description='High-performance sports cars.')

print("Creating Brands...")
toyota = Brand.objects.create(name='Toyota', slug='toyota', country_of_origin='Japan')
ford = Brand.objects.create(name='Ford', slug='ford', country_of_origin='USA')
tesla = Brand.objects.create(name='Tesla', slug='tesla', country_of_origin='USA')
bmw = Brand.objects.create(name='BMW', slug='bmw', country_of_origin='Germany')
honda = Brand.objects.create(name='Honda', slug='honda', country_of_origin='Japan')

print("Creating Cars...")
cars_to_create = [
    Car(brand=tesla, category=electric, model_name='Model 3', slug='model-3', year=2023, price=38990.00, mileage=150, transmission='AUTOMATIC', fuel_type='ELECTRIC', color='Pearl White', description='Long range electric sedan with autopilot capabilities.', stock=3, is_available=True),
    
    Car(brand=toyota, category=suv, model_name='RAV4', slug='rav4', year=2022, price=28900.00, mileage=12000, transmission='AUTOMATIC', fuel_type='HYBRID', color='Magnetic Gray', description='Reliable and spacious hybrid SUV, perfect for families.', stock=2, is_available=True),
    
    Car(brand=ford, category=truck, model_name='F-150', slug='f-150', year=2021, price=45000.00, mileage=25000, transmission='AUTOMATIC', fuel_type='GAS', color='Agate Black', description='Best-selling full-size pickup truck with great towing capacity.', stock=1, is_available=True),
    
    Car(brand=bmw, category=sports, model_name='M4', slug='m4', year=2023, price=72000.00, mileage=500, transmission='AUTOMATIC', fuel_type='GAS', color='Isle of Man Green', description='High-performance luxury sports coupe with a twin-turbo engine.', stock=1, is_available=True),
    
    Car(brand=honda, category=sedan, model_name='Civic', slug='civic', year=2020, price=22000.00, mileage=35000, transmission='CVT', fuel_type='GAS', color='Rallye Red', description='Compact, reliable, and incredibly fuel-efficient daily driver.', stock=4, is_available=True),
]

# Bulk create is faster than creating them one by one
Car.objects.bulk_create(cars_to_create)

print("✅ Dummy data successfully created! Check your admin panel.")