from django.urls import path, include

from .views import views
from .views.report_views import all_reports

app_name = "dashboard"

urls_reports = [
    path(r"monthly/", view=all_reports.report_monthly, name="report_monthly"),
    path(r"weekly/", view=all_reports.report_weekly, name="report_weekly"),
    path(r"yearly/", view=all_reports.report_yearly, name="report_yearly"),
    path(r"zones/", view=all_reports.report_zones, name="report_zones"),
    path(r"community/", view=all_reports.report_community, name="report_community"),
]

urlpatterns = [
    path("", view=views.home_view),
    path("import-xls/<slug:file_type>/", view=views.upload_file, name="upload_file"),
    path("change-period/", view=views.change_anual_period, name="change_anual_period"),
    path(r"api/", include(views.router.urls)),
    path(r"reports/", include(urls_reports)),
]
