# Generated by Django 5.1.7 on 2025-03-16 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_forest', '0003_alter_forestmodel_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forestclassificationmodel',
            old_name='array_map',
            new_name='forest_mask',
        ),
    ]
