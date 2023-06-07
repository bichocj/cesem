from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from .utils.import_data.import_data_animals import ImportAnimals
from .utils.import_data.import_data_grass import ImportGrass
from .api_views.people import PersonViewSet, PersonPathSerializer
from .api_views.users import UserViewSet, UserPathSerializer
from .api_views.zones import ZoneViewSet, ZonePathSerializer
from .api_views.sectores import SectorViewSet, SectorPathSerializer
from .api_views.communities import CommunityViewSet, CommunityPathSerializer
from .api_views.activities import ActivityViewSet, ActivityPathSerializer
from .api_views.visits_animals import VisitAnimalViewSet, VisitAnimalPathSerializer
from .api_views.visits_grass import VisitGrassViewSet, VisitGrassPathSerializer
from .api_views.diagnostics import DiagnosticViewSet, DiagnosticPathSerializer
from .api_views.sickness_observations import (
    SicknessObservationViewSet,
    SicknessObservationPathSerializer,
)
from .api_views.drugs import DrugPathSerializer, DrugViewSet
from .api_views.production_units import (
    ProductionUnitPathSerializer,
    ProductionUnitViewSet,
)


@login_required
def home_view(request):
    message = "Hello"
    return render(request, "dashboard/home.html", locals())


@login_required
def upload_file(request, file_type):
    if "POST" == request.method:
        excel_file = request.FILES["excel_file"]
        if file_type == "animal":
            importer = ImportAnimals()
        elif file_type == "pasto":
            importer = ImportGrass()
        importer.execute(excel_file, True)
    return render(request, "dashboard/import_visits.html", locals())


people_path = PersonPathSerializer.get_path()
visit_path = VisitAnimalPathSerializer.get_path()
visit_grass_path = VisitGrassPathSerializer.get_path()
diagnistic_path = DiagnosticPathSerializer.get_path()
sickness_observations_path = SicknessObservationPathSerializer.get_path()
activities_path = ActivityPathSerializer.get_path()
communities_path = CommunityPathSerializer.get_path()
drugs_path = DrugPathSerializer.get_path()
production_units_path = ProductionUnitPathSerializer.get_path()

router = routers.DefaultRouter()
router.register(
    r"%s" % UserPathSerializer.get_path(),
    UserViewSet,
)
router.register(r"%s" % people_path, PersonViewSet, basename=people_path)
router.register(r"%s" % ZonePathSerializer.get_path(), ZoneViewSet)
router.register(r"%s" % SectorPathSerializer.get_path(), SectorViewSet)
router.register(r"%s" % communities_path, CommunityViewSet, basename=communities_path)
router.register(r"%s" % activities_path, ActivityViewSet, basename=activities_path)
router.register(r"%s" % visit_path, VisitAnimalViewSet, basename=visit_path)
router.register(r"%s" % visit_grass_path, VisitGrassViewSet, basename=visit_grass_path)
router.register(r"%s" % diagnistic_path, DiagnosticViewSet, basename=diagnistic_path)
router.register(
    r"%s" % sickness_observations_path,
    SicknessObservationViewSet,
    basename=sickness_observations_path,
)
router.register(r"%s" % drugs_path, DrugViewSet, basename=drugs_path)
router.register(
    r"%s" % production_units_path, ProductionUnitViewSet, basename=production_units_path
)
