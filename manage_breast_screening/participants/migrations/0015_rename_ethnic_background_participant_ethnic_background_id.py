# Generated by Django 5.2.3 on 2025-06-27 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0014_alter_appointmentstatus_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='ethnic_background',
            new_name='ethnic_background_id',
        ),
    ]
