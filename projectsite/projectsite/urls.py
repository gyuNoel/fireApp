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
    FireStationView,
    FireStationCreateView,
    FireStationUpdateView,
    FireStationDeleteView,
    FirefightersView,
    FirefightersCreateView,
    FirefightersUpdateView,
    FirefightersDeleteView,
    FiretruckView,
    FiretruckCreateView,
    FiretruckUpdateView,
    FiretruckDeleteView,
    LocationsView,
    LocationsCreateView,
    LocationsUpdateView,
    LocationsDeleteView,
    IncidentsView,
    IncidentsCreateView,
    IncidentsUpdateView,
    IncidentsDeleteView,
    WeatherConditionsView,
    WeatherConditionsCreateView,
    WeatherConditionsUpdateView,
    WeatherConditionsDeleteView,
)
from fire import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    # charts
    path("dashboard_chart", ChartView.as_view(), name="dashboard-chart"),
    path("chart/", PieCountbySeverity, name="chart"),
    path("lineChart/", LineCountbyMonth, name="chart"),
    path("multilineChart/", MultilineIncidentTop3Country, name="chart"),
    path("multiBarChart/", multipleBarbySeverity, name="chart"),
    path("map-station", views.map_station, name="map-station"),
    path("stations/", map_station, name="map-station"),
    path("fire_incidents/", fire_incident_map, name="fire-incidents"),
    # Fire Station
    path("firestation_list", FireStationView.as_view(), name="firestation-list"),
    path(
        "firestation_list/add", FireStationCreateView.as_view(), name="firestation-add"
    ),
    path(
        "firestation_list/<pk>",
        FireStationUpdateView.as_view(),
        name="firestation-update",
    ),
    path(
        "firestation_list/<pk>/delete",
        FireStationDeleteView.as_view(),
        name="firestation-delete",
    ),
    # Firefighters
    path("firefighters_list", FirefightersView.as_view(), name="firefighters-list"),
    path(
        "firefighters_list/add",
        FirefightersCreateView.as_view(),
        name="firefighters-add",
    ),
    path(
        "firefighters_list/<pk>",
        FirefightersUpdateView.as_view(),
        name="firestation-update",
    ),
    path(
        "firefighters_list/<pk>/delete",
        FirefightersDeleteView.as_view(),
        name="firefighters-delete",
    ),
    # Firetruck
    path("firetruck_list", FiretruckView.as_view(), name="firetruck-list"),
    path("firetruck_list/add", FiretruckCreateView.as_view(), name="firetruck-add"),
    path(
        "firetruck_list/<pk>",
        FiretruckUpdateView.as_view(),
        name="firetruck-update",
    ),
    path(
        "firetruck_list/<pk>/delete",
        FiretruckDeleteView.as_view(),
        name="firetruck-delete",
    ),
    # Locations
    path("locations_list", LocationsView.as_view(), name="locations-list"),
    path("locations_list/add", LocationsCreateView.as_view(), name="locations-add"),
    path(
        "locations_list/<pk>",
        LocationsUpdateView.as_view(),
        name="locations-update",
    ),
    path(
        "firestation_list/<pk>/delete",
        LocationsDeleteView.as_view(),
        name="locations-delete",
    ),
    # Incidents
    path("incidents_list", IncidentsView.as_view(), name="incidents-list"),
    path("incidents_list/add", IncidentsCreateView.as_view(), name="incidents-add"),
    path(
        "incidents_list/<pk>",
        IncidentsUpdateView.as_view(),
        name="incidents-update",
    ),
    path(
        "incidents_list/<pk>/delete",
        IncidentsDeleteView.as_view(),
        name="incidents-delete",
    ),
    # Weather Conditions
    path(
        "weathercondition_list",
        WeatherConditionsView.as_view(),
        name="weathercondition-list",
    ),
    path(
        "weathercondition_list/add",
        WeatherConditionsCreateView.as_view(),
        name="weathercondition-add",
    ),
    path(
        "weathercondition_list/<pk>",
        WeatherConditionsUpdateView.as_view(),
        name="weathercondition-update",
    ),
    path(
        "weathercondition_list/<pk>/delete",
        WeatherConditionsDeleteView.as_view(),
        name="weathercondition-delete",
    ),
]
