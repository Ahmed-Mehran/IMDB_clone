# Generated by Django 5.0.6 on 2024-09-06 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_watchlist_average_rating_watchlist_total_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='sum_of_rating',
            field=models.FloatField(default=0),
        ),
    ]
