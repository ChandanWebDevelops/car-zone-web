# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse 

from django.views.generic import ListView, DetailView
from django.views import View
from .forms import OrderCreateForm
from .models import Car, OrderItem, Order
from .cart import Cart # Import our new Cart class

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            return redirect('store:car_list')
    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {'form':form})


# Profile View (Protected: Login Required)
@login_required
def profile(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/profile.html', {'orders':orders})


class CarListView(ListView):
    model = Car
    template_name = 'store/car_list.html'
    context_object_name = 'cars'
    paginate_by = 9

class CarDetailView(DetailView):
    model = Car
    template_name = 'store/car_detail.html'
    context_object_name = 'car'

# --- NEW CART VIEWS ---

class CartAddView(View):
    def get(self, request, id):
        cart = Cart(request)
        car = get_object_or_404(Car, id=id)
        cart.add(car=car)
        return redirect('store:cart_detail')

class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'store/cart.html', {'cart': cart})

class CartRemoveView(View):
    def get(self, request, id):
        cart = Cart(request)
        car = get_object_or_404(Car, id=id)
        cart.remove(car)
        return redirect('store:cart_detail')

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1. Save the order details
            order = form.save(commit=False) # Don't save to DB yet
            # If the user is logged in, attach their account to the order

            if request.user.is_authenticated:
                order.user = request.user

            order.save() # Now save to DB
            # 2. Create order items for each car in the cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    car=item['car'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                
            # 3. Clear the cart session
            cart.clear()
            
            # 4. Redirect to a success page
            # return render(request, 'store/ordered.html', {'order': order})
            # New Logic
            request.session['order_id'] = order.id
            return redirect('store:payment_process')
    else:
        form = OrderCreateForm()
        
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


# store/views.py (Add to the bottom)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    # Debug: Print order details
    print(f"Order ID: {order.id}")
    print(f"Order Items Count: {order.items.count()}")
    
    # Get the total cost
    total_cost = order.get_total_cost()
    print(f"Total Cost: {total_cost}")
    
    # Stripe requires amounts in cents (e.g., $50.00 = 5000)
    total_cost_in_cents = int(total_cost * 100)
    
    # If total is 0, use a fallback (this shouldn't happen but just in case)
    if total_cost_in_cents == 0:
        # Try to get price from the first order item
        first_item = order.items.first()
        if first_item:
            total_cost_in_cents = int(first_item.price * 100)
            print(f"Using fallback price: {first_item.price}")

    # Create a Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',  # Change to 'usd' for USD
                'product_data': {
                    'name': f'Car Order #{order.id} - {order.first_name} {order.last_name}',
                },
                'unit_amount': total_cost_in_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('store:payment_success')) + f'?order_id={order.id}',
        cancel_url=request.build_absolute_uri(reverse('store:payment_cancel')),
    )
    
    return redirect(checkout_session.url, code=303)

def payment_success(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    # Mark the order as paid!
    order.paid = True
    order.save()
    # Clear the cart only after successful payment
    cart = Cart(request)
    cart.clear()
    
    # Clear the order ID from session
    if 'order_id' in request.session:
        del request.session['order_id']
        
    return render(request, 'store/payment/success.html', {'order': order})


def payment_cancel(request):
    return render(request, 'store/payment/cancel.html')