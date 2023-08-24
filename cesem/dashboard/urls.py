from django.urls import path, include

from .views import views
from .views.report_views import animal_view

app_name = "dashboard"

urls_reports = [
    path(r"monthly/", view=animal_view.report_monthly, name="report_monthly"),
    path(r"weekly/", view=animal_view.report_weekly, name="report_weekly"),
    path(r"zones/", view=animal_view.report_zones, name="report_zones"),
    path(r"community/", view=animal_view.report_community, name="report_community"),
]

urlpatterns = [
    path("", view=views.home_view),
    path("import-xls/<slug:file_type>/", view=views.upload_file, name="upload_file"),
    path(r"api/", include(views.router.urls)),
    path(r"reports/", include(urls_reports)),
]
