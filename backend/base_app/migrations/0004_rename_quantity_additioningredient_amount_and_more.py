# Generated by Django 4.0.5 on 2022-09-23 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_rename_title_tag_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='additioningredient',
            old_name='quantity',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit_of_measurement',
            new_name='measurement_unit',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
    ]
