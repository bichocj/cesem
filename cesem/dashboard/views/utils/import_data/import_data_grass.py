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
        self.columns_names = [
            "N°",
            "MES",  #
            "FECHA",
            "ZONA",
            "COMUNIDAD ",
            "SECTOR/IRRIGACION",
            "NOMBRE RESPONSABLE UP",
            "Nº DNI",
            "SEXO RUP",
            "NOMBRE DEL INTEGRANTE DE LA UP",
            "Nº DNI.1",
            "SEXO IUP",
            "COORDENADAS UTM Anuales",
            # "LA UP ESTA BASE DE DATOS?",
            # "UP DE MONITOREO",
            # "UP  ES PILOTO?",
            # "TIPIFICACION\nde productores (A-B-C)",
            "NOMBRE RESPONSABLE",
            "RESPONSABLE DE ACTIVIDAD",
            "ACTIVIDAD REALIZADA",
            "HAS, INTENS, \nSIEMBRA",
            # "ANAL.\nSUELO",
            # "HORAS \nARADO",
            # "HORAS \nRASTRA",
            # "KG AVENA",
            # "KG VICIA",
            # "KG. ALFALFA",
            # "KG. DACTYLIS",
            # "KG RAYGRASS",
            # "KG TREBOL B",
            # "FERTILIZANTE (Bolsas x 50 kg) ",
            "HAS. SIEMBRA \nAVENA/VICIA",
            "HAS. SIEMBRA\n ALFALFA DACTYLIS",
            "HAS. SIEMBRA \nRAYGRASS TREBOL",
            "EVAL.COSECH. \nKG MV/HA",
            "ASISTENCIA \nTECNICA",
            "PASTOREO DIRECTO (%)",
            "HENO (%)",
            "ENSILADO (%)",
            "PACAS (%)",
            "PASTOREO %\nPERENNE",
            "RENDIMIENTO\nPERENNE",
            "CAPACITACION INTALACION PERENNES",
        ]

    def _inner_execute(self, file, creates_if_none=True):
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
            data_up_responsable_dni = self.zero_if_nan(
                self.nan_if_nat(data["Nº DNI"][i])
            )
            data_up_responsable_sex = self.nan_if_nat(data["SEXO RUP"][i])
            data_up_member_name = self.nan_if_nat(
                data["NOMBRE DEL INTEGRANTE DE LA UP"][i]
            )
            data_up_member_dni = self.zero_if_nan(self.nan_if_nat(data["Nº DNI.1"][i]))
            data_up_member_sex = self.nan_if_nat(data["SEXO IUP"][i])
            data_anual_utm_coordinates = self.nan_if_nat(
                data["COORDENADAS UTM Anuales"][i]
            )
            data_employ_responsable = self.nan_if_nat(data["NOMBRE RESPONSABLE"][i])
            data_employ_specialist = self.nan_if_nat(
                data["RESPONSABLE DE ACTIVIDAD"][i]
            )
            data_activity = self.nan_if_nat(data["ACTIVIDAD REALIZADA"][i])
            #
            data_planting_intention_hectares = self.zero_if_nan(
                data["HAS, INTENS, \nSIEMBRA"][i]
            )
            data_avena_vicia_planted_hectares = self.zero_if_nan(
                data["HAS. SIEMBRA \nAVENA/VICIA"][i]
            )
            data_alfalfa_dactylis_planted_hectares = self.zero_if_nan(
                data["HAS. SIEMBRA\n ALFALFA DACTYLIS"][i]
            )
            data_raygrass_trebol_planted_hectares = self.zero_if_nan(
                data["HAS. SIEMBRA \nRAYGRASS TREBOL"][i]
            )
            data_direct_grazing = self.zero_if_nan(data["PASTOREO DIRECTO (%)"][i])
            data_hay = self.zero_if_nan(data["HENO (%)"][i])
            data_ensilage = self.zero_if_nan(data["ENSILADO (%)"][i])
            data_bale = self.zero_if_nan(data["PACAS (%)"][i])
            data_perennial_grazing = self.zero_if_nan(data["PASTOREO %\nPERENNE"][i])
            data_perennial_yield = self.zero_if_nan(data["RENDIMIENTO\nPERENNE"][i])
            # activities
            data_harvest_evaluation = self.zero_if_nan(
                data["EVAL.COSECH. \nKG MV/HA"][i]
            )
            data_technical_assistance = self.zero_if_nan(
                data["ASISTENCIA \nTECNICA"][i]
            )
            data_technical_training = self.zero_if_nan(
                data["CAPACITACION INTALACION PERENNES"][i]
            )

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
                        planting_intention_hectares=data_planting_intention_hectares,
                        avena_vicia_planted_hectares=data_avena_vicia_planted_hectares,
                        alfalfa_dactylis_planted_hectares=data_alfalfa_dactylis_planted_hectares,
                        raygrass_trebol_planted_hectares=data_raygrass_trebol_planted_hectares,
                        direct_grazing=data_direct_grazing,
                        hay=data_hay,
                        ensilage=data_ensilage,
                        bale=data_bale,
                        perennial_grazing=data_perennial_grazing,
                        perennial_yield=data_perennial_yield,
                    )
                )
                # check if new visits need to be created because of more activities
                if data_harvest_evaluation and data_harvest_evaluation != "nan":
                    visits.append(
                        VisitGrass(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=self.get_activity("EVAL. COSECH. KG MV/HA", True),
                            quantity=float(data_harvest_evaluation),
                        )
                    )

                if data_technical_assistance and data_technical_assistance != "nan":
                    visits.append(
                        VisitGrass(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=self.get_activity("ASISTENCIA TECNICA", True),
                            quantity=float(data_technical_assistance),
                        )
                    )

                if data_technical_training or data_technical_training != "nan":
                    visits.append(
                        VisitGrass(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=self.get_activity(
                                "CAPACITACION INSTALACION PERENNES", True
                            ),
                            quantity=float(data_technical_training),
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
        return len(visits)
