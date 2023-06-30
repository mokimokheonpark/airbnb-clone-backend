# Generated by Django 4.2.2 on 2023-06-30 21:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='payload',
            new_name='review',
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveBigIntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
