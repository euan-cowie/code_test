from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IATACodeFilter
from .models import Flight, Segment, Airport
from .serializers import (
    FlightSerializer, SegmentSerializer, AirportSerializer
)


# TODO - separate client/server (this is for simple render)
def index(request):
    return render(request, 'code_test/index.html', {})


class AirportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filterset_fields = ('iso_country', 'continent',)


class FlightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filterset_class = IATACodeFilter

    @action(detail=False)
    def count(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        content = {
            'count': count
        }
        return Response(content)


class SegmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer


class FlightSegmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SegmentSerializer

    def get_queryset(self):
        return Segment.objects.filter(flight=self.kwargs['flight_pk'])
