# Generated by Django 4.2.2 on 2023-07-01 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_room_category'),
        ('experiences', '0002_experience_category_alter_perk_description_and_more'),
        ('wishlists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='experiences',
            field=models.ManyToManyField(blank=True, to='experiences.experience'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='rooms',
            field=models.ManyToManyField(blank=True, to='rooms.room'),
        ),
    ]
