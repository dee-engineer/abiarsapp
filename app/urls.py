from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('signup/', views.userregister, name='signup'),
    path('logout/', views.userlogout, name='logout'),
    path('home/', views.home, name='home'),
    path('initiate_payment/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('paystack/', views.paystack, name='paystack'),
]