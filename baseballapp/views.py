from django.shortcuts import render
from baseballapp.models import GameModel, PlayerModel
from rest_framework import viewsets
from .serializers import PlayerSerializer
from rest_framework import filters

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = PlayerModel.objects.all()  # Fetch all PlayerModel instances
    serializer_class = PlayerSerializer  # Specify the serializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'team']  # Allow sorting by name or team
    ordering = ['name']  # Default ordering by name
# Create your views here.
from .serializers import TeamModelSerializer
from .models import TeamModel
class TeamModelViewSet(viewsets.ModelViewSet):
    queryset = TeamModel.objects.all()
    serializer_class = TeamModelSerializer

def game(request):
    games = GameModel.objects.all()
    return render(request, 'baseballapp/game.html', locals())

