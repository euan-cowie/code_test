from rest_framework import serializers
from .models import Flight, Segment, Airport


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request')

        if request:
            fields = request.query_params.get('fields')
            if fields:
                fields = fields.split(',')
                # Drop any fields that are not specified in the `fields` argument.
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


class AirportSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = (
            'iata_code', 'name', 'continent', 'iso_country',
        )


class SegmentSerializer(serializers.ModelSerializer):
    dep_code = AirportSerializer(many=False)
    arr_code = AirportSerializer(many=False)

    class Meta:
        model = Segment
        fields = (  # TODO - Could be __all__ if no fine tuning
            'id', 'flight_id', 'dep_code', 'arr_code', 'dep_date',
            'arr_date', 'dep_time', 'arr_time', 'dep_terminal',
            'arr_terminal', 'flight_no', 'journey', 'seg_class',
            'booking_class',
        )


class FlightSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    segments = SegmentSerializer(many=True, source='segment_set')
    dep_air = AirportSerializer(many=False)
    dest_air = AirportSerializer(many=False)
    in_depart_code = AirportSerializer(many=False)
    in_arrive_code = AirportSerializer(many=False)

    class Meta:
        model = Flight
        fields = (  # TODO - Could be __all__ if no fine tuning
            'id', 'dep_air', 'dest_air', 'in_depart_code',
            'in_arrive_code', 'out_flight_no', 'out_depart_date',
            'out_depart_time', 'out_arrival_date', 'out_arrival_time',
            'out_booking_class', 'out_flight_class', 'out_carrier_code',
            'in_flight_no', 'in_depart_date', 'in_depart_time',
            'in_arrival_date', 'in_arrival_time', 'in_booking_class',
            'in_flight_class', 'in_carrier_code', 'original_price',
            'original_currency', 'reservation', 'carrier', 'oneway',
            'segments',
        )
