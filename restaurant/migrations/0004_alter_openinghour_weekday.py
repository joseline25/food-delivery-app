# Generated by Django 5.0 on 2023-12-07 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_openinghour_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='weekday',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')]),
        ),
    ]