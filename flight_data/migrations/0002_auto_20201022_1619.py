# Generated by Django 3.1.2 on 2020-10-22 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='in_arrive_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_arrive_code_airport', to='flight_data.airport'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='in_depart_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_depart_code_airport', to='flight_data.airport'),
        ),
    ]
