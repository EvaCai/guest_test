# Generated by Django 2.2.2 on 2019-06-15 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest',
            old_name='creat_time',
            new_name='create_time',
        ),
    ]