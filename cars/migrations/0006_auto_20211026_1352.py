# Generated by Django 3.2.3 on 2021-10-26 11:52

import cars.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_delete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='car_engine_power',
            field=models.PositiveSmallIntegerField(validators=[cars.models.validate_car_engine_power]),
        ),
        migrations.AlterField(
            model_name='cars',
            name='num_of_passengers',
            field=models.PositiveSmallIntegerField(validators=[cars.models.validate_num_of_passengers]),
        ),
        migrations.AlterField(
            model_name='cars',
            name='year_of_production',
            field=models.PositiveSmallIntegerField(validators=[cars.models.validate_year]),
        ),
    ]
