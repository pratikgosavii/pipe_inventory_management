# Generated by Django 4.1.5 on 2023-04-03 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0038_outward_mobile_no_outward_name_of_buyer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outward',
            name='name_of_buyer',
        ),
    ]