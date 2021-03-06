# Generated by Django 2.0.7 on 2018-09-20 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showtimes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screening',
            name='cinema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cinemas', to='showtimes.Cinema'),
        ),
        migrations.AlterField(
            model_name='screening',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='movielist.Movie'),
        ),
    ]
