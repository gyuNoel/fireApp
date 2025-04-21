from django.contrib import admin
from django.urls import path

from fire.views import (
    HomePageView,
    ChartView,
    PieCountbySeverity,
    LineCountbyMonth,
    MultilineIncidentTop3Country,
    multipleBarbySeverity,
    map_station,
    fire_incident_map,
)
from fire import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("dashboard_chart", ChartView.as_view(), name="dashboard-chart"),
    path("chart/", PieCountbySeverity, name="chart"),
    path("multilineChart/", MultilineIncidentTop3Country, name="chart"),
    path("multiBarChart/", multipleBarbySeverity, name="chart"),
    path("map-station", views.map_station, name="map-station"),
    path("stations/", map_station, name="map-station"),
    path("fire_incidents/", fire_incident_map, name="fire-incidents"),
]
