from django.urls import path, include

from .views import views
from .views.report_views import animal_view

app_name = "dashboard"

urls_reports = [
    path(r"animals/", view=animal_view.report, name="reports_animals"),
]

urlpatterns = [
    path("", view=views.home_view),
    path("import-xls/<slug:file_type>/", view=views.upload_file, name="upload_file"),
    path(r"api/", include(views.router.urls)),
    path(r"reports/", include(urls_reports)),
]
