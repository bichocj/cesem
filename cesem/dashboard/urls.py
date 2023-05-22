from django.urls import path, include

from .import_data import import_animal_visits, import_grass_visits
from . import views
from .report_views import animal_view

app_name = "dashboard"

urls_reports = [
    path(r"animals/", view=animal_view.report, name="reports_animals"),
    path(
        r"import-animal-visits/",
        view=import_animal_visits.upload_file,
        name="import_animal_visits",
    ),
    path(
        r"import-grass-visits/",
        view=import_grass_visits.upload_file,
        name="import_grass_visits",
    ),
]

urlpatterns = [
    path("", view=views.home_view),
    path(r"api/", include(views.router.urls)),
    path(r"reports/", include(urls_reports)),
]
