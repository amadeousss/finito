# Generated by Django 4.0.3 on 2022-04-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster_url',
            field=models.URLField(default='https://m.media-amazon.com/images/M/MV5BMzA0YWMwMTUtMTVhNC00NjRkLWE2ZTgtOWEzNjJhYzNiMTlkXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg'),
            preserve_default=False,
        ),
    ]
