from django.contrib import admin
from baseballapp.models import PlayerModel, PitcherModel, HitterModel, TeamModel, GameModel
# Register your models here.
admin.site.register(TeamModel)
admin.site.register(PlayerModel)
admin.site.register(PitcherModel)
admin.site.register(HitterModel)

admin.site.register(GameModel)