from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Airport(models.Model):
    iata_code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=256, null=False)
    continent = models.CharField(max_length=2, null=False)
    iso_country = models.CharField(max_length=2, null=False)


class Flight(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    dep_air = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='dep_air_airport')
    dest_air = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='dest_air_airport')
    in_depart_code = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='in_depart_code_airport')
    in_arrive_code = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='in_arrive_code_airport')
    out_flight_no = models.CharField(max_length=32, null=False)
    out_depart_date = models.DateField(null=True, blank=True)
    out_depart_time = models.TimeField(null=True, blank=True)
    out_arrival_date = models.DateField(null=True, blank=True)
    out_arrival_time = models.TimeField(null=True, blank=True)
    out_booking_class = models.CharField(max_length=256, null=True)
    out_flight_class = models.CharField(max_length=64, null=False)
    out_carrier_code = models.CharField(max_length=2, null=True)
    in_flight_no = models.CharField(max_length=32, null=False)
    in_depart_date = models.DateField(null=True, blank=True)
    in_depart_time = models.TimeField(null=True, blank=True)
    in_arrival_date = models.DateField(null=True, blank=True)
    in_arrival_time = models.TimeField(null=True, blank=True)
    in_booking_class = models.CharField(max_length=256, null=True)
    in_flight_class = models.CharField(max_length=64, null=False)
    in_carrier_code = models.CharField(max_length=2, null=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    original_currency = models.CharField(max_length=3, null=False)
    reservation = models.CharField(max_length=32, null=False)
    carrier = models.CharField(max_length=64, null=False)
    oneway = models.BooleanField()


class Segment(models.Model):
    class Journey(models.TextChoices):
        OUT = 'out', _('Out')
        IN = 'in', _('In')

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    dep_code = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='dep_code_airport')
    arr_code = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arr_code_airport')
    dep_date = models.DateField(null=True, blank=True)
    arr_date = models.DateField(null=True, blank=True)
    dep_time = models.TimeField(null=True, blank=True)
    arr_time = models.TimeField(null=True, blank=True)
    dep_terminal = models.CharField(max_length=32, null=True)
    arr_terminal = models.CharField(max_length=32, null=True)
    flight_no = models.CharField(max_length=32, null=False)
    journey = models.CharField(max_length=3, choices=Journey.choices, default=Journey.OUT)
    seg_class = models.CharField(max_length=64, null=False)
    booking_class = models.CharField(max_length=256, null=True)
