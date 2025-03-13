import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from .utils.import_data.import_data_animals import ImportAnimals
from .utils.import_data.import_data_grass import ImportGrass
from .utils.import_data.import_data_component_2 import ImportComponent2
from .utils.import_data.import_data_component_3 import ImportComponent3
from .api_views.people import PersonViewSet, PersonPathSerializer
from .api_views.users import UserViewSet, UserPathSerializer
from .api_views.zones import ZoneViewSet, ZonePathSerializer
from .api_views.sectores import SectorViewSet, SectorPathSerializer
from .api_views.communities import CommunityViewSet, CommunityPathSerializer
from .api_views.activities import ActivityViewSet, ActivityPathSerializer
from .api_views.visits_animals import (
    VisitAnimalHealthViewSet,
    VisitAnimalHealthPathSerializer,
)
from .api_views.visits_dewormed import (
    VisitAnimalDewormingViewSet,
    VisitAnimalDewormedPathSerializer,
)
from .api_views.visits_vacuno import (
    VisitGeneticImprovementVacunoViewSet,
    VisitGeneticImprovementVacunoPathSerializer,
)
from .api_views.visits_ovino import (
    VisitGeneticImprovementOvinoViewSet,
    VisitGeneticImprovementOvinoPathSerializer,
)
from .api_views.visits_alpaca import (
    VisitGeneticImprovementAlpacaViewSet,
    VisitGeneticImprovementAlpacaPathSerializer,
)

from .api_views.visits_grass import VisitGrassViewSet, VisitGrassPathSerializer
from .api_views.visits_component_2 import (
    VisitComponent2ViewSet,
    VisitComponent2PathSerializer,
)
from .api_views.visits_component_3 import (
    VisitComponent3ViewSet,
    VisitComponent3PathSerializer,
)
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
from .api_views.files_checksum import FilesChecksumPathSerializer, FilesChecksumViewSet
from core.models import AnualPeriod


@login_required
def home_view(request):
    # message = "Hello"
    return render(request, "dashboard/home.html", locals())


@login_required
def user_search(request):
    return render(request, "dashboard/user_search.html", locals())


@login_required
def upload_file(request, file_type):
    if "POST" == request.method:
        excel_file = request.FILES["excel_file"]
        try:
            if file_type == "animales":
                importer = ImportAnimals()
            elif file_type == "pastos":
                importer = ImportGrass()
            elif file_type == "componente2":
                importer = ImportComponent2()
            elif file_type == "componente3":
                importer = ImportComponent3()
            rows = importer.execute(excel_file, True)
            message_success = "Se registraron {} filas".format(str(rows))
        except KeyError as e:
            message_error = f"No se encontró el campo {e}, compruebe que en el Excel no tenga espacios en blanco"
        except Exception as e:
            message_error = str(e)
    return render(request, "dashboard/import_visits.html", locals())


@login_required
def change_anual_period(request):
    from_anual_period_object = AnualPeriod.objects.first()
    from_anual_period = from_anual_period_object.date_from

    # verificando si el from se trata de una fecha que solo existe en bisiesto
    if from_anual_period.month == 2 and from_anual_period.day == 29:
        to_anual_period = datetime.date(from_anual_period.year + 1, 2, 28)
    else:
        to_anual_period = from_anual_period.replace(
            year=from_anual_period.year + 1
        ) - datetime.timedelta(days=1)

    if "POST" == request.method:
        from_anual_period_str = request.POST.get("from_anual_period")
        from_anual_period = datetime.datetime.strptime(
            from_anual_period_str, "%Y-%m-%d"
        ).date()

        from_anual_period_object.date_from = from_anual_period
        from_anual_period_object.save()

        # verificando si el from se trata de una fecha que solo existe en bisiesto
        if from_anual_period.month == 2 and from_anual_period.day == 29:
            to_anual_period = datetime.date(from_anual_period.year + 1, 2, 28)
        else:
            to_anual_period = from_anual_period.replace(
                year=from_anual_period.year + 1
            ) - datetime.timedelta(days=1)

    return render(request, "dashboard/anual_period.html", locals())


people_path = PersonPathSerializer.get_path()
visit_path = VisitAnimalHealthPathSerializer.get_path()
deworming_path = VisitAnimalDewormedPathSerializer.get_path()
visit_grass_path = VisitGrassPathSerializer.get_path()
diagnistic_path = DiagnosticPathSerializer.get_path()
sickness_observations_path = SicknessObservationPathSerializer.get_path()
activities_path = ActivityPathSerializer.get_path()
communities_path = CommunityPathSerializer.get_path()
drugs_path = DrugPathSerializer.get_path()
production_units_path = ProductionUnitPathSerializer.get_path()
files_checksum_path = FilesChecksumPathSerializer.get_path()
visit_vacuno_path = VisitGeneticImprovementVacunoPathSerializer.get_path()
visit_ovino_path = VisitGeneticImprovementOvinoPathSerializer.get_path()
visit_alpaca_path = VisitGeneticImprovementAlpacaPathSerializer.get_path()
visit_component_2_path = VisitComponent2PathSerializer.get_path()
visit_component_3_path = VisitComponent3PathSerializer.get_path()

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
router.register(r"%s" % visit_path, VisitAnimalHealthViewSet, basename=visit_path)
router.register(
    r"%s" % deworming_path, VisitAnimalDewormingViewSet, basename=deworming_path
)
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
router.register(
    r"%s" % files_checksum_path, FilesChecksumViewSet, basename=files_checksum_path
)
router.register(
    r"%s" % visit_vacuno_path,
    VisitGeneticImprovementVacunoViewSet,
    basename=visit_vacuno_path,
)
router.register(
    r"%s" % visit_ovino_path,
    VisitGeneticImprovementOvinoViewSet,
    basename=visit_ovino_path,
)
router.register(
    r"%s" % visit_alpaca_path,
    VisitGeneticImprovementAlpacaViewSet,
    basename=visit_alpaca_path,
)
router.register(
    r"%s" % visit_component_2_path,
    VisitComponent2ViewSet,
    basename=visit_component_2_path,
)
router.register(
    r"%s" % visit_component_3_path,
    VisitComponent3ViewSet,
    basename=visit_component_3_path,
)
