from core.models import Activity, VisitAnimal
from django.shortcuts import render

from dashboard.import_data.import_data_grass import ImportGrass


def upload_file(request):
    if "GET" == request.method:
        return render(request, "dashboard/import_grass_visits.html", {})
    else:
        excel_file = request.FILES["excel_file"]
        grass_instance = ImportGrass()
        grass_instance.execute(excel_file, True)
        return render(request, "dashboard/import_grass_visits.html", {})
