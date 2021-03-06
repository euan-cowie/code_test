# Generated by Django 3.1.2 on 2020-10-22 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight_data', '0002_auto_20201022_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='in_arrive_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_arrive_code_airport', to='flight_data.airport'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='in_depart_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_depart_code_airport', to='flight_data.airport'),
        ),
    ]
