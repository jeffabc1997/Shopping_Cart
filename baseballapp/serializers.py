from rest_framework import serializers
from .models import PlayerModel
from .models import TeamModel

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerModel
        fields = '__all__'  # Include all fields from the PlayerModel


class TeamModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamModel
        fields = '__all__'