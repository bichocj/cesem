from django.urls import path, include

from .views import views
from .views.report_views import animal_view

app_name = "dashboard"

urls_reports = [
    path(r"weekly/", view=animal_view.report_weekly, name="reports_weekly"),
    path(r"zones/", view=animal_view.report_zones, name="reports_zones"),
]

urlpatterns = [
    path("", view=views.home_view),
    path("import-xls/<slug:file_type>/", view=views.upload_file, name="upload_file"),
    path(r"api/", include(views.router.urls)),
    path(r"reports/", include(urls_reports)),
]
