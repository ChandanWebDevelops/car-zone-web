from django.core.management.base import BaseCommand
from store.models import Car, Brand, Category

class Command(BaseCommand):
    help = 'Seeds the database with initial car inventory'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing car data...')
        Car.objects.all().delete()

        self.stdout.write('Creating brands and categories...')
        
        # 1. Create Brands
        tesla, _ = Brand.objects.get_or_create(name='Tesla')
        ford, _ = Brand.objects.get_or_create(name='Ford')
        bmw, _ = Brand.objects.get_or_create(name='BMW')
        toyota, _ = Brand.objects.get_or_create(name='Toyota')
        porsche, _ = Brand.objects.get_or_create(name='Porsche')

        # 2. Create Categories
        sedan, _ = Category.objects.get_or_create(name='Sedan')
        suv, _ = Category.objects.get_or_create(name='SUV')
        sports, _ = Category.objects.get_or_create(name='Sports Car')
        truck, _ = Category.objects.get_or_create(name='Truck')

        self.stdout.write('Adding cars to the inventory...')
        
        # 3. Define the Cars Data
                # 3. Define the Cars Data (NOW WITH SLUGS!)
        cars_data = [
            {'brand': tesla, 'model': 'Model S', 'slug': 'tesla-model-s', 'price': 89990, 'cat': sedan, 'year': 2023, 'mileage': 1500, 'trans': 'A', 'fuel': 'E', 'stock': 5},
            {'brand': tesla, 'model': 'Model X', 'slug': 'tesla-model-x', 'price': 99990, 'cat': suv, 'year': 2023, 'mileage': 2000, 'trans': 'A', 'fuel': 'E', 'stock': 3},
            {'brand': ford, 'model': 'F-150 Raptor', 'slug': 'ford-f150-raptor', 'price': 75000, 'cat': truck, 'year': 2022, 'mileage': 5000, 'trans': 'A', 'fuel': 'P', 'stock': 4},
            {'brand': ford, 'model': 'Mustang GT', 'slug': 'ford-mustang-gt', 'price': 45000, 'cat': sports, 'year': 2023, 'mileage': 3000, 'trans': 'M', 'fuel': 'P', 'stock': 6},
            {'brand': bmw, 'model': 'M4 Competition', 'slug': 'bmw-m4-competition', 'price': 82000, 'cat': sports, 'year': 2023, 'mileage': 1000, 'trans': 'A', 'fuel': 'P', 'stock': 2},
            {'brand': bmw, 'model': 'X5 xDrive', 'slug': 'bmw-x5-xdrive', 'price': 65000, 'cat': suv, 'year': 2022, 'mileage': 8000, 'trans': 'A', 'fuel': 'P', 'stock': 5},
            {'brand': toyota, 'model': 'Camry XSE', 'slug': 'toyota-camry-xse', 'price': 32000, 'cat': sedan, 'year': 2023, 'mileage': 1200, 'trans': 'A', 'fuel': 'H', 'stock': 10},
            {'brand': toyota, 'model': 'RAV4 Hybrid', 'slug': 'toyota-rav4-hybrid', 'price': 38000, 'cat': suv, 'year': 2023, 'mileage': 2500, 'trans': 'A', 'fuel': 'H', 'stock': 8},
            {'brand': porsche, 'model': '911 Carrera', 'slug': 'porsche-911-carrera', 'price': 115000, 'cat': sports, 'year': 2023, 'mileage': 500, 'trans': 'A', 'fuel': 'P', 'stock': 1},
            {'brand': porsche, 'model': 'Cayenne', 'slug': 'porsche-cayenne', 'price': 85000, 'cat': suv, 'year': 2022, 'mileage': 4000, 'trans': 'A', 'fuel': 'P', 'stock': 3},
        ]

        # 4. Insert the Cars
        for data in cars_data:
            Car.objects.create(
                brand=data['brand'],
                model_name=data['model'],
                slug=data['slug'],  # <--- ADD THIS LINE!
                price=data['price'],
                category=data['cat'],
                year=data['year'],
                mileage=data['mileage'],
                transmission=data['trans'],
                fuel_type=data['fuel'],
                is_available=True,  
                stock=data['stock'] 
            )
        # 5. Success Message
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully seeded {len(cars_data)} cars into the database!'))