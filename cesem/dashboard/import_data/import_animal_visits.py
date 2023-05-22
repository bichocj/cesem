from core.models import Activity, VisitAnimal
from django.shortcuts import render

from dashboard.import_data.import_data_animals import ImportAnimals


def upload_file(request):
    if "GET" == request.method:
        return render(request, "dashboard/import_animal_visits.html", {})
    else:
        excel_file = request.FILES["excel_file"]
        animals_instance = ImportAnimals()
        animals_instance.execute(excel_file, True)
        return render(request, "dashboard/import_animal_visits.html", {})
