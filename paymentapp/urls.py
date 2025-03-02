from django.urls import path

from . import views

urlpatterns = [
    # path('', views.paymentapp),
    path('payment/', views.payment),
    path('payment-success/<int:orderid>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:orderid>/', views.paymentFailed, name='payment-failed'),
]