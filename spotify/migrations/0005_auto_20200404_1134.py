# Generated by Django 3.0.3 on 2020-04-04 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0004_auto_20200404_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifydata',
            name='access_token',
            field=models.CharField(max_length=256),
        ),
    ]
