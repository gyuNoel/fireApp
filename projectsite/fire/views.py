from django.shortcuts import render
from django.views.generic.list import ListView
from fire.models import (
    Locations,
    Incident,
    FireStation,
    Firefighters,
    FireTruck,
    WeatherConditions,
)
from django.db import connection
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.urls import reverse_lazy
from fire.forms import (
    LocationsForm,
    IncidentsForms,
    FireStationForm,
    FireFightersForm,
    FireTruckForm,
    WeatherConditionsForm,
)

from django.db.models import Count
from datetime import datetime
from django.contrib import messages


class HomePageView(ListView):
    model = Locations
    context_object_name = "home"
    template_name = "home.html"


class ChartView(ListView):
    template_name = "chart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        pass


def PieCountbySeverity(request):
    query = """
    SELECT severity_level, COUNT (*) as count
    FROM fire_incident
    GROUP BY severity_level
    """
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    if rows:
        # Construct the dictionary with severity level as keys and count as values
        data = {severity: count for severity, count in rows}
    else:
        data = {}

    return JsonResponse(data)


def LineCountbyMonth(request):
    current_year = datetime.now().year
    result = {month: 0 for month in range(1, 13)}

    incidents_per_month = Incident.objects.filter(
        date_time__year=current_year
    ).values_list("date_time", flat=True)

    # Counting the number of incidents per month
    for date_time in incidents_per_month:
        month = date_time.month
        result[month] += 1

    # IF you want to convert month numbers to month names, you can use a dictionary mapping
    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    result_with_month_names = {
        month_names[int(month)]: count for month, count in result.items()
    }
    return JsonResponse(result_with_month_names)


def MultilineIncidentTop3Country(request):
    query = """
    SELECT
        fl.country,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM
        fire_incident fi
    JOIN
        fire_locations fl ON fi.location_id = fl.id
    WHERE
        fl.country IN (
            SELECT
                fl_top.country
            FROM
                fire_incident fi_top
            JOIN
                fire_locations fl_top ON fi_top.location_id = fl_top.id
            WHERE
                strftime('%Y', fi_top.date_time) = strftime('%Y', 'now')
            GROUP BY
                fl_top.country
            ORDER BY
                COUNT(fi_top.id) DESC
            LIMIT 3
        )   
        AND strftime('%Y', fi.date_time) = strftime('%Y', 'now')
    GROUP BY
        fl.country, month
    ORDER BY
        fl.country, month;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Initialize a dictionary to store the result
    result = {}

    # Initialize a set of months from January to December
    months = set(str(i).zfill(2) for i in range(1, 13))

    # Loop through the query results
    for row in rows:
        country = row[0]
        month = row[1]
        total_incidents = row[2]

        # If the country is not in the result dictionary, initialize it with all months set to zero
        if country not in result:
            result[country] = {month: 0 for month in months}

        # Update the incidents count for the corresponding month
        result[country][month] = total_incidents

    # Ensure there are always 3 countries in the result
    while len(result) < 3:
        # Placeholder name for missing countries
        missing_country = f"Country {len(result) + 1}"
        result[missing_country] = {month: 0 for month in months}

    for country in result:
        result[country] = dict(sorted(result[country].items()))

    return JsonResponse(result)


def multipleBarbySeverity(request):
    query = """
    SELECT
        fi.severity_level,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM
        fire_incident fi
    GROUP BY fi.severity_level, month
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = {}
    months = {str(i).zfill(2) for i in range(1, 13)}

    for row in rows:
        level = str(row[0])  # Ensure the severity level is a string
        month = row[1]
        total_incidents = row[2]

        if level not in result:
            result[level] = {month: 0 for month in months}

        result[level][month] = total_incidents

        # Sort months within each severity level
        for level in result:
            result[level] = dict(sorted(result[level].items()))

    return JsonResponse(result)


def map_station(request):
    fireStations = FireStation.objects.values("name", "latitude", "longitude")

    for fs in fireStations:
        fs["latitude"] = float(fs["latitude"])
        fs["longitude"] = float(fs["longitude"])

    fireStations_list = list(fireStations)
    context = {
        "fireStations": fireStations_list,
    }
    return render(request, "map_station.html", context)


def fire_incident_map(request):

    fireIncidents = Locations.objects.values("name", "latitude", "longitude")
    for fs in fireIncidents:
        fs["latitude"] = float(fs["latitude"])
        fs["longitude"] = float(fs["longitude"])

    fireIncidents_list = list(fireIncidents)

    context = {
        "fireIncidents": fireIncidents_list,
    }

    return render(request, "fire_incident_map.html", context)


class FireStationView(ListView):
    model = FireStation
    context_object_name = "Fire Station"
    template_name = "firestation_list.html"
    paginate_by = 5


class FireStationCreateView(CreateView):
    model = FireStation
    form_class = FireStationForm
    template_name = "firestation_add.html"
    success_url = reverse_lazy("firestation-list")

    def form_valid(self, form):
        messages.success(self.request, "Fire station added successfully!")
        return super().form_valid(form)


class FireStationUpdateView(UpdateView):
    model = FireStation
    form_class = FireStationForm
    template_name = "firestation_edit.html"
    success_url = reverse_lazy("firestation-list")

    def form_valid(self, form):
        messages.success(self.request, "Fire station updated successfully!")
        return super().form_valid(form)


class FireStationDeleteView(DeleteView):
    model = FireStation
    template_name = "firestation_delete.html"
    success_url = reverse_lazy("firestation-list")

    def form_valid(self, form):
        messages.success(self.request, "Fire station deleted successfully!")
        return super().form_valid(form)


class FirefightersView(ListView):
    model = Firefighters
    context_object_name = "Firefighters"
    template_name = "firefighters_list.html"
    paginate_by = 5


class FirefightersCreateView(CreateView):
    model = Firefighters
    form_class = FireFightersForm
    template_name = "firefighters_add.html"
    success_url = reverse_lazy("firefighters-list")

    def form_valid(self, form):
        messages.success(self.request, "Firefighter added successfully!")
        return super().form_valid(form)


class FirefightersUpdateView(UpdateView):
    model = Firefighters
    form_class = FireFightersForm
    template_name = "firefighters_edit.html"
    success_url = reverse_lazy("firefighters-list")

    def form_valid(self, form):
        messages.success(self.request, "Firefighter updated successfully!")
        return super().form_valid(form)


class FirefightersDeleteView(DeleteView):
    model = Firefighters
    template_name = "firefighters_delete.html"
    success_url = reverse_lazy("firefighters-list")

    def form_valid(self, form):
        messages.success(self.request, "Firefighter deleted successfully!")
        return super().form_valid(form)


class FiretruckView(ListView):
    model = FireTruck
    context_object_name = "Firetruck"
    template_name = "firetruck_list.html"
    paginate_by = 5


class FiretruckCreateView(CreateView):
    model = FireTruck
    form_class = FireTruckForm
    template_name = "firetruck_add.html"
    success_url = reverse_lazy("firetruck-list")

    def form_valid(self, form):
        messages.success(self.request, "Fire truck added successfully!")
        return super().form_valid(form)


class FiretruckUpdateView(UpdateView):
    model = FireTruck
    form_class = FireTruckForm
    template_name = "firetruck_edit.html"
    success_url = reverse_lazy("firetruck-list")

    def form_valid(self, form):
        messages.success(self.request, "Fire truck updated successfully!")
        return super().form_valid(form)


class FiretruckDeleteView(DeleteView):
    model = FireTruck
    template_name = "firetruck_delete.html"
    success_url = reverse_lazy("firetruck-list")

    def form_valid(self, form):
        messages.success(self.request, "Fire truck deleted successfully!")
        return super().form_valid(form)


class LocationsView(ListView):
    model = Locations
    context_object_name = "Locations"
    template_name = "location_list.html"
    paginate_by = 5


class LocationsCreateView(CreateView):
    model = Locations
    form_class = LocationsForm
    template_name = "location_add.html"
    success_url = reverse_lazy("locations-list")

    def form_valid(self, form):
        messages.success(self.request, "Location added successfully!")
        return super().form_valid(form)


class LocationsUpdateView(UpdateView):
    model = Locations
    form_class = LocationsForm
    template_name = "location_edit.html"
    success_url = reverse_lazy("locations-list")

    def form_valid(self, form):
        messages.success(self.request, "Location updated successfully!")
        return super().form_valid(form)


class LocationsDeleteView(DeleteView):
    model = Locations
    template_name = "location_delete.html"
    success_url = reverse_lazy("locations-list")

    def form_valid(self, form):
        messages.success(self.request, "Location deleted successfully!")
        return super().form_valid(form)


class IncidentsView(ListView):
    model = Incident
    context_object_name = "Incidents"
    template_name = "incident_list.html"
    paginate_by = 5


class IncidentsCreateView(CreateView):
    model = Incident
    form_class = IncidentsForms
    template_name = "incident_add.html"
    success_url = reverse_lazy("incidents-list")

    def form_valid(self, form):
        messages.success(self.request, "Incident added successfully!")
        return super().form_valid(form)


class IncidentsUpdateView(UpdateView):
    model = Incident
    form_class = IncidentsForms
    template_name = "incident_edit.html"
    success_url = reverse_lazy("incidents-list")

    def form_valid(self, form):
        messages.success(self.request, "Incident updated successfully!")
        return super().form_valid(form)


class IncidentsDeleteView(DeleteView):
    model = Incident
    template_name = "incident_delete.html"
    success_url = reverse_lazy("incidents-list")

    def form_valid(self, form):
        messages.success(self.request, "Incident deleted successfully!")
        return super().form_valid(form)


class WeatherConditionsView(ListView):
    model = WeatherConditions
    context_object_name = "Weather Conditions"
    template_name = "weathercondition_list.html"
    paginate_by = 5


class WeatherConditionsCreateView(CreateView):
    model = WeatherConditions
    form_class = WeatherConditionsForm
    template_name = "weathercondition_add.html"
    success_url = reverse_lazy("weathercondition-list")

    def form_valid(self, form):
        messages.success(self.request, "Weather condition added successfully!")
        return super().form_valid(form)


class WeatherConditionsUpdateView(UpdateView):
    model = WeatherConditions
    form_class = WeatherConditionsForm
    template_name = "weathercondition_edit.html"
    success_url = reverse_lazy("weathercondition-list")

    def form_valid(self, form):
        messages.success(self.request, "Weather condition updated successfully!")
        return super().form_valid(form)


class WeatherConditionsDeleteView(DeleteView):
    model = WeatherConditions
    template_name = "weathercondition_delete.html"
    success_url = reverse_lazy("weathercondition-list")

    def form_valid(self, form):
        messages.success(self.request, "Weather condition deleted successfully!")
        return super().form_valid(form)
