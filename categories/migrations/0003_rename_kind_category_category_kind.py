# Generated by Django 4.2.2 on 2023-07-01 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_alter_category_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='kind',
            new_name='category_kind',
        ),
    ]
