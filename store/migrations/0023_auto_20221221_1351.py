# Generated by Django 3.2.15 on 2022-12-21 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20220223_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterUniqueTogether(
            name='agent',
            unique_together={('company', 'name')},
        ),
    ]
