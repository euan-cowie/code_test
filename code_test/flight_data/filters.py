from django_filters import Filter, FilterSet
from .models import Flight


class ListFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)


class IATACodeFilter(FilterSet):
    dep_air = ListFilter(field_name='dep_air')
    dest_air = ListFilter(field_name='dest_air')
    out_flight_class = ListFilter(field_name='out_flight_class')

    class Meta:
        model = Flight
        fields = ['dep_air', 'dest_air', 'out_flight_class']
