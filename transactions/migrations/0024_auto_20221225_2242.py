# Generated by Django 3.2.15 on 2022-12-25 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_transport'),
        ('transactions', '0023_auto_20221221_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='inward',
            name='bill_no',
            field=models.BigIntegerField(default=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outward',
            name='bill_no',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inward',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sdv', to='store.agent'),
        ),
        migrations.AlterField(
            model_name='outward',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='df', to='store.agent'),
        ),
    ]
