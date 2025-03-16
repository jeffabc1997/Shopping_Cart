from django.urls import path

from . import views

urlpatterns = [
    # path('', views.paymentapp),
    path('game/', views.game), 
    path('', views.game),
]# Compare this snippet from baseballapp/views.py: