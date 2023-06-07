import os
from django.conf import settings
from core.models import (
    Activity,
    Community,
    Diagnostic,
    Drug,
    SicknessObservation,
    Zone,
    VisitGrass,
    Sector,
    ProductionUnit,
)
import pandas as pd

from .utils import HelperImport

baset_path = os.path.join(settings.BASE_DIR, "core", "management", "commands", "files")


class ImportGrass(HelperImport):
    help = "import xls data"
    diagnostic_names = {}
    sickness_observation_names = {}

    def __init__(self):
        super().__init__()

    def nan_if_nat(self, val):
        if type(val) is pd._libs.tslibs.nattype.NaTType:
            return "nan"
        else:
            return val

    def none_if_nat(self, val):
        if type(val) is pd._libs.tslibs.nattype.NaTType:
            return None
        else:
            return val

    def execute(self, file, creates_if_none=True):
        # path = os.path.join(baset_path, file)
        # columns format ['Nº', 'MES', 'FECHA', 'ZONA', 'COMUNIDAD ', 'PDE-2019', 'SECTOR/IRRIGACION DE LA UP ', 'TIPOLOGIA DE UP', 'UP  ES PILOTO?', 'NOMBRE RESPONSABLE UP', 'Nº DNI', 'SEXO RUP', 'NOMBRE DEL INTEGRANTE DE LA UP', 'Nº DNI.1', 'SEXO IUP', 'SECTOR/IRRIGACION DEL BENEFICIARIO', 'NOMBRE DE ESPECIALISTA', 'RESPONSABLE DE ACTIVIDAD', 'ACTIVIDAD REALIZADA', 'SECCION 1', 'ENFERMEDAD/TRANSTORNO/OBSERVACION', 'DIAGNOSTICO', 'VACA', 'VAQUILLONA', 'VAQUILLA', 'TERNERO', 'TORETE', 'TORO', 'VACUNOS', 'OVINOS', 'ALPACAS', 'LLAMAS', 'CANES', '1 FARMACOS /SALES', 'CANTIDAD', 'U.M.', '2 FARMACOS /SALES', 'CANTIDAD.1', 'U.M..1', '3 FARMACOS /SALES', 'CANTIDAD.2', 'U.M..2', '4 FARMACOS /SALES', 'CANTIDAD.3', 'U.M..3']
        # the order and names should be the same in xls file
        df = pd.read_excel(file)
        data = df.to_dict()
        rows_count = len(data["N°"].keys())
        visits = []

        for i in range(rows_count):
            data_visited_at = self.none_if_nat(data["FECHA"][i])
            data_zone = self.nan_if_nat(data["ZONA"][i])
            data_community = self.nan_if_nat(data["COMUNIDAD "][i])
            data_sector = self.nan_if_nat(data["SECTOR/IRRIGACION"][i])
            data_up_responsable_name = self.nan_if_nat(data["NOMBRE RESPONSABLE UP"][i])
            data_up_responsable_dni = self.nan_if_nat(data["Nº DNI"][i])
            data_up_responsable_sex = self.nan_if_nat(data["SEXO RUP"][i])
            data_up_member_name = self.nan_if_nat(
                data["NOMBRE DEL INTEGRANTE DE LA UP"][i]
            )
            data_up_member_dni = self.nan_if_nat(data["Nº DNI.1"][i])
            data_up_member_sex = self.nan_if_nat(data["SEXO IUP"][i])
            data_anual_utm_coordinates = self.nan_if_nat(
                data["COORDENADAS UTM Anuales"][i]
            )
            data_employ_responsable = self.nan_if_nat(data["NOMBRE RESPONSABLE"][i])
            data_employ_specialist = self.nan_if_nat(
                data["RESPONSABLE DE ACTIVIDAD"][i]
            )
            data_activity = self.nan_if_nat(data["ACTIVIDAD REALIZADA"][i])
            # TODO: work on activity quantities

            try:
                employ_responsable = self.get_person(data_employ_responsable)
                employ_specialist = self.get_person(data_employ_specialist)
                activity = self.get_activity(data_activity, creates_if_none)
                production_unit = self.get_production_unit(
                    data_zone,
                    data_community,
                    data_sector,
                    data_up_responsable_name,
                    data_up_responsable_dni,
                    data_up_responsable_sex,
                    data_up_member_name,
                    data_up_member_dni,
                    data_up_member_sex,
                    creates_if_none=True,
                )

                visits.append(
                    VisitGrass(
                        visited_at=data_visited_at,
                        production_unit=production_unit,
                        employ_specialist=employ_specialist,
                        employ_responsable=employ_responsable,
                        activity=activity,
                        utm_coordenate=data_anual_utm_coordinates,
                    )
                )
                print("Registrando visita de pastos Nº: ", i + 1)

            except Zone.DoesNotExist:
                print("row", str(i + 1), "not found zone:", data_zone)
                exit()
            except Community.DoesNotExist:
                print("row", str(i + 1), "not found community:", data_community)
                exit()
            except Sector.DoesNotExist:
                print("row", str(i + 1), "not found sector:", data_sector)
                exit()
            except Activity.DoesNotExist:
                print("row", str(i + 1), "not found activity:", data_activity)
                exit()

        VisitGrass.objects.bulk_create(visits)
