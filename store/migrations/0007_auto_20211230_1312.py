# Generated by Django 3.0.8 on 2021-12-30 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20211230_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_goods',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]
