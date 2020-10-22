from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from flight_data import views

router = DefaultRouter()
router.register(r'flights', views.FlightViewSet)
router.register(r'segments', views.SegmentViewSet)
router.register(r'airports', views.AirportViewSet)

flights_router = routers.NestedSimpleRouter(router, r'flights', lookup='flight')
flights_router.register(r'segments', views.FlightSegmentViewSet, basename='flight-segments')

urlpatterns = [
    path('', views.index),
    path('api/', include(router.urls)),
    path('api/', include(flights_router.urls)),
]
