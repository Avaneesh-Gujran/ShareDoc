# Generated by Django 4.2.16 on 2024-11-16 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='document',
            name='shared_with',
        ),
    ]
