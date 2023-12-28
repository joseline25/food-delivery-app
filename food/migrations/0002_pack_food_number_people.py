# Generated by Django 5.0 on 2023-12-27 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number_of_people', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='number_people',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]