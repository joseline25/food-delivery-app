# Generated by Django 5.0 on 2023-12-07 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_openinghour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='weekday',
            field=models.IntegerField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]),
        ),
    ]