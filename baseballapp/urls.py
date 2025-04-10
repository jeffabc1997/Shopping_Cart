from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, TeamModelViewSet
router = DefaultRouter()
router.register(r'players', PlayerViewSet)  # Register the PlayerViewSet with the URL 'players/'
router.register(r'teams', TeamModelViewSet, basename='team')

urlpatterns = [
    # path('', views.paymentapp),
    path('game/', views.game), 
    path('', views.game),
     path('api/', include(router.urls)),  # Include the router's URLs in your main URL
]# Compare this snippet from baseballapp/views.py: