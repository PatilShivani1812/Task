# Generated by Django 4.2.2 on 2023-12-02 11:18

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_order_order_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(2023, 12, 2))]),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=25)]),
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'product')},
        ),
    ]
