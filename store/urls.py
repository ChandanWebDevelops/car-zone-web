# store/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('car/<int:id>/<slug:slug>/', views.CarDetailView.as_view(), name='car_detail'),
    
    # Cart URLs
    path('cart/add/<int:id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/remove/<int:id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('checkout/', views.order_create, name='order_create'),

    # Authentication Urls
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # We will user Django's Built in Login/Logout views for simplicity
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='store:car_list'), name='logout'),

    # Payment URLs
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),

]