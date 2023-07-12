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

# anual_yield
# direct_grazing
# hay
# ensilage
# bale
# perennial_grazing
# Sperennial_yield

mapping_activity_quantity = {
    "PASTOS ASISTENCIA TECNICA EN MANEJO DE PASTOS": "technical_assistance",
    "PASTOS EVALUACION DE COSECHA PASTOS ANUALES": "",
    "PASTOS EVALUACION DE COSECHA PASTOS ANUALES CEGADO MOTOGUADAÑA": "",
    "PASTOS EVALUACION DE COSECHA PASTOS PERENNES RENDIMIENTO": "",
    "PASTOS EVALUACION DE INTENSION DE SIEMBRA ANUALES": "planting_intention_hectares",
    "PASTOS EVALUACION DE INTENSION DE SIEMBRA PERENNES": "",
    "PASTOS INST. PAST ANUALES ARADO": "plow_hours",
    "PASTOS INST. PAST ANUALES RASTRA": "dredge_hours",
    "PASTOS INST. PAST. PERENNES ALFALFA Y DACTYLIS": "alfalfa_dactylis_planted_hectares",
    "PASTOS INST. PAST. PERENNES ANALISIS DE SUELO": "ground_analysis",  # no hay para anuales
    "PASTOS INST. PAST. PERENNES ARADO": "",  #
    "PASTOS INST. PAST. PERENNES DISTRIBUION SEMILLA": "",
    "PASTOS INST. PAST. PERENNES RASTRA": "",
    "PASTOS INST. PAST. PERENNES RYEGRASS Y TREBOL": "raygrass_trebol_planted_hectares",
    "PASTOS INST. PAST. ANUALES AVENA Y VICIA": "avena_vicia_planted_hectares",
    "PASTOS INST. PAST. ANUALES ENTREGA FERTILIZANTE": "fertilizer",  # solo para anuales
    "PASTOS INTS. PAST. ANUALES DISTRIBUCION SEMILLA": "oat_kg",  # vicia_kg
    "PASTOS DISTRIBUCION PERENNES ALFALFA": "alfalfa_kg",  # dactylis_kg No presente en matriz
    "PASTOS DISTRIBUCION PERENNES DACTYLIS": "dactylis_kg",
    "PASTOS DISTRIBUCION PERENNES RYEGRASS Y TREBOL": "ryegrass_kg",  # trebol_b_kg No presente en matriz
    "PASTOS CURSO TALLER EN INSTALACION DE PASTOS PERENNES": "technical_training",
}


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
            # NOMBRE RESPONSABLE INICIAL, nuevo campo en xls
            # NOMBRE RESPONSABLE OFICIAL, nuevo campo en xls, es el mismo que NOMBRE RESPONSABLE UP?
            "NOMBRE RESPONSABLE UP",
            "Nº DNI",
            "SEXO RUP",
            "NOMBRE DEL INTEGRANTE DE LA UP",  # no presente en xls
            "Nº DNI.1",  # no presente en xls
            "SEXO IUP",  # no presente en xls
            "COORDENADAS UTM Anuales",
            # "LA UP ESTA BASE DE DATOS?", se va a quitar
            # "UP DE MONITOREO", se va a quitar
            # "UP  ES PILOTO?", se va a quitar
            "TIPIFICACION\nde productores (A-B-C)",
            "NOMBRE RESPONSABLE",
            "RESPONSABLE DE ACTIVIDAD",
            "ACTIVIDAD REALIZADA",
            "HAS. INTENS. \nSIEMBRA",
            "ANAL.\nSUELO",
            "HORAS \nARADO",
            "HORAS \nRASTRA",
            "KG AVENA",
            "KG VICIA",
            "KG. ALFALFA",
            "KG. DACTYLIS",
            "KG RAYGRASS",
            "KG TREBOL B",
            "FERTILIZANTE (Bolsas x 50 kg) ",
            "HAS. SIEMBRA \nAVENA/VICIA",
            "HAS. SIEMBRA\n ALFALFA DACTYLIS",
            "HAS. SIEMBRA \nRAYGRASS TREBOL",
            "RENDIMIENTO ANUALES KG MV/HA",  # EVAL.COSECH. \nKG MV/HA
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
            data_producer_classification = self.nan_if_nat(
                data["TIPIFICACION de productores (A-B-C)"][i]
            )
            data_employ_responsable = self.nan_if_nat(data["NOMBRE RESPONSABLE"][i])
            data_employ_specialist = self.nan_if_nat(
                data["RESPONSABLE DE ACTIVIDAD"][i]
            )
            data_activity = self.nan_if_nat(data["ACTIVIDAD REALIZADA"][i])
            #
            data_planting_intention_hectares = self.zero_if_nan(
                data["HAS. INTENS. \nSIEMBRA"][i]
            )
            data_ground_analysis = self.zero_if_nan(data["ANAL. SUELO"][i])
            data_plow_hours = self.zero_if_nan(data["HORAS ARADO"][i])
            data_dredge_hours = self.zero_if_nan(data["HORAS RASTRA"][i])
            data_oat_kg = self.zero_if_nan(data["KG AVENA"][i])
            data_vicia_kg = self.zero_if_nan(data["KG VICIA"][i])
            data_alfalfa_kg = self.zero_if_nan(data["KG ALFALFA"][i])
            data_dactylis_kg = self.zero_if_nan(data["KG DACTYLIS"][i])
            data_ryegrass_kg = self.zero_if_nan(data["KG RYEGRASS"][i])
            data_trebol_b_kg = self.zero_if_nan(data["KG TREBOL B"][i])
            data_fertilizer = self.zero_if_nan(data["FERTILIZANTE (Bolsas x 50 kg)"][i])
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
            data_anual_yield = self.zero_if_nan(data["RENDIMIENTO ANUALES KG MV/HA"][i])
            data_technical_assistance = self.zero_if_nan(
                data["ASISTENCIA \nTECNICA"][i]
            )
            data_technical_training = self.zero_if_nan(
                data["CAPACITACION INSTALACION PERENNES"][i]
            )

            mapping_activity_detail = {
                "planting_intention_hectares": data_planting_intention_hectares,
                "ground_analysis": data_ground_analysis,
                "plow_hours": data_plow_hours,
                "dredge_hours": data_dredge_hours,
                "oat_kg": data_oat_kg,
                "vicia_kg": data_vicia_kg,
                "alfalfa_kg": data_alfalfa_kg,
                "dactylis_kg": data_dactylis_kg,
                "ryegrass_kg": data_ryegrass_kg,
                "trebol_b_kg": data_trebol_b_kg,
                "fertilizer": data_fertilizer,
                "avena_vicia_planted_hectares": data_avena_vicia_planted_hectares,
                "alfalfa_dactylis_planted_hectares": data_alfalfa_dactylis_planted_hectares,
                "raygrass_trebol_planted_hectares": data_raygrass_trebol_planted_hectares,
                "technical_assistance": data_technical_assistance,
                "anual_yield": data_anual_yield,
                "direct_grazing": data_direct_grazing,
                "hay": data_hay,
                "ensilage": data_ensilage,
                "bale": data_bale,
                "perennial_grazing": data_perennial_grazing,
                "perennial_yield": data_perennial_yield,
                "technical_training": data_technical_training,
            }

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
                        utm_coordenate=data_anual_utm_coordinates,
                        producer_classification=data_producer_classification,
                        employ_specialist=employ_specialist,
                        employ_responsable=employ_responsable,
                        activity=activity,
                        quantity=mapping_activity_detail.get(
                            mapping_activity_quantity.get(activity)
                        ),
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
