# Generated by Django 4.2.19 on 2025-03-15 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseballapp', '0002_alter_playermodel_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammodel',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teammodel',
            name='ops',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='teammodel',
            name='wins',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='GameModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('date', models.DateField(default='2000-01-01')),
                ('game_pk', models.IntegerField(default=-1)),
                ('away_starting_pitcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_starting_pitcher', to='baseballapp.pitchermodel')),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='baseballapp.teammodel')),
                ('home_starting_pitcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_starting_pitcher', to='baseballapp.pitchermodel')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='baseballapp.teammodel')),
            ],
        ),
    ]
