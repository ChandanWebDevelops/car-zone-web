# store/cart.py
from decimal import Decimal
from django.conf import settings
from .models import Car

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        # If there is no cart in the session, create an empty one
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
            
        self.cart = cart

    def add(self, car, quantity=1, override_quantity=False):
        """
        Add a car to the cart or update its quantity.
        """
        car_id = str(car.id)
        if car_id not in self.cart:
            self.cart[car_id] = {
                'quantity': 0,
                'price': str(car.price)
            }
            
        if override_quantity:
            self.cart[car_id]['quantity'] = quantity
        else:
            self.cart[car_id]['quantity'] += quantity
            
        self.save()

    def save(self):
        # Mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, car):
        """
        Remove a car from the cart.
        """
        car_id = str(car.id)
        if car_id in self.cart:
            del self.cart[car_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the cars from the database.
        """
        car_ids = self.cart.keys()
        cars = Car.objects.filter(id__in=car_ids)
        cart = self.cart.copy()
        
        for car in cars:
            cart[str(car.id)]['car'] = car

        for item in cart.values():
            item = item.copy() 
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total cost of the items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove the entire cart.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()