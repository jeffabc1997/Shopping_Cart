from django.shortcuts import render
from baseballapp.models import GameModel
# Create your views here.

def game(request):
    games = GameModel.objects.all()
    return render(request, 'baseballapp/game.html', locals())