from django.db import models

# Create your models here.
class TeamModel(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=5)
    ops = models.FloatField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default = 0)

    def __str__(self):
        return self.name
    
class PlayerModel(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(TeamModel, null=True, blank=True, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    mlbid = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class PitcherModel(models.Model):
    player = models.OneToOneField(PlayerModel, on_delete=models.CASCADE)
    era = models.FloatField(default=0)
    strikeouts = models.IntegerField(default=0)

    def __str__(self):
        return self.player.name

class HitterModel(models.Model):
    player = models.OneToOneField(PlayerModel, on_delete=models.CASCADE)
    batting_average = models.FloatField(default=0)
    home_runs = models.IntegerField(default=0)
    rbis = models.IntegerField(default=0)

    def __str__(self):
        return self.player.name
     
class GameModel(models.Model):
    home_team = models.ForeignKey(TeamModel, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(TeamModel, related_name='away_team', on_delete=models.CASCADE)
    home_starting_pitcher = models.ForeignKey(PitcherModel, on_delete=models.CASCADE, related_name='home_starting_pitcher', null=True, blank=True)
    away_starting_pitcher = models.ForeignKey(PitcherModel, on_delete=models.CASCADE, related_name='away_starting_pitcher', null=True, blank=True)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    date = models.DateField(default='2000-01-01')
    game_pk = models.IntegerField(default=-1)

    def __str__(self):
        return f'{self.home_team} vs {self.away_team} on {self.date}'