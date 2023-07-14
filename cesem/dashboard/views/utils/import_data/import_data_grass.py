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

mapping_activity_quantity = {
    "instalación de parcelas de avena forrajera asociado con vicia": "avena_vicia_planted_hectares",
    "entrega de semilla de avena tayco": "oat_kg",
    "entrega de semillas de vicia": "vicia_kg",
    "instalación de alfalfa + dactylis": "alfalfa_dactylis_planted_hectares",
    "instalación de rye grass + trébol blanco": "ryegrass_trebol_planted_hectares",
    "entrega de semilla de alfalfa (25 Kg/Ha)": "alfalfa_kg",
    "entrega de semilla de dactylis (5 Kg/Ha)": "dactylis_kg",
    "entrega de semilla de ryegrass (20 Kg/Ha)": "ryegrass_kg",
    "entrega de semilla de trébol blanco (5 Kg/Ha)": "trebol_b_kg",
    # "adquisición de fertilizante fosforado (02 bolsas/ha) Zona 9": "fertilizer",
    "curso taller en instalación de pastos anuales y perennes (parcelas demostrativas)": [
        "technical_training_perennial",
        "technical_training_anual",
    ],
    "curso taller en manejo y conservación de forrajes cultivados": "technical_training_conservation",
    "asistencia técnica": "technical_assistance",
    "evaluación de intensión de siembra de cultivos anuales y perennes": "planting_intention_hectares",
    "evaluación de cosecha de pastos cultivados anuales (monitoreo)": "anual_yield",
    "evaluación de cosecha de pastos cultivados perennes (monitoreo)": "perennial_yield",
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
            "COMUNIDAD",
            "SECTOR/IRRIGACION",
            # NOMBRE RESPONSABLE INICIAL, nuevo campo en xls
            # NOMBRE RESPONSABLE OFICIAL, nuevo campo en xls, es el mismo que NOMBRE RESPONSABLE UP?
            "NOMBRE DEL RESPONSABLE UP",
            "Nº DNI",
            "SEXO RUP",
            "NOMBRE DEL INTEGRANTE DE UP",  # no presente en xls
            "Nº DNI.1",  # no presente en xls
            "SEXO IUP",  # no presente en xls
            "COORDENADAS UTM ANUALES",
            # "LA UP ESTA BASE DE DATOS?", se va a quitar
            # "UP DE MONITOREO", se va a quitar
            # "UP  ES PILOTO?", se va a quitar
            "TIPIFICACION DE PRODUCTORES (A-B-C)",
            "NOMBRE DE RESPONSABLE",
            "NOMBRE DE RESPONSABLE DE ACTIVIDAD",
            "ACTIVIDAD REALIZADA",
            "HAS. INTENS. DE SIEMBRA",
            "ANAL.SUELO",
            "HORAS ARADO",
            "HORAS RASTRA",
            "KG AVENA",
            "KG VICIA",
            "KG ALFALFA",
            "KG DACTYLIS",
            "KG RYEGRASS",
            "KG TREBOL",
            "FERTILIZANTE (BOLSAS X 50 KG)",
            "HAS. SIEMBRA AVENA/VICIA",
            "HAS. SIEMBRA ALFALFA DACTYLIS",
            "HAS. SIEMBRA RYEGRASS TREBOL",
            "RENDIMIENTO ANUALES KG MV/HA",  # EVAL.COSECH. \nKG MV/HA
            "ASISTENCIA TECNICA",
            "PASTOREO DIRECTO (%)",
            "HENO (%)",
            "ENSILADO (%)",
            "PACAS (%)",
            "PASTOREO % PERENNE",
            "ENSILADO % PERENNE",
            "RENDIMIENTO PERENNE",
            "CAPACITACION INSTALACION PERENNES",
            "CAPACITACION INSTALACION ANUALES",
            "CAPACITACION MANEJO Y CONSERVACION",
        ]

    def _inner_execute(self, file, creates_if_none=True):
        df = pd.read_excel(file)
        data = df.to_dict()
        rows_count = len(data["N°"].keys())
        visits = []

        for i in range(rows_count):
            data_visited_at = self.none_if_nat(data["FECHA"][i])
            data_zone = self.nan_if_nat(data["ZONA"][i])
            data_community = self.nan_if_nat(data["COMUNIDAD"][i])
            data_sector = self.nan_if_nat(data["SECTOR/IRRIGACION"][i])
            data_up_responsable_name = self.nan_if_nat(
                data["NOMBRE DEL RESPONSABLE UP"][i]
            )
            data_up_responsable_dni = self.zero_if_nan(
                self.nan_if_nat(data["N° DNI"][i])
            )
            data_up_responsable_sex = self.nan_if_nat(data["SEXO RUP"][i])
            data_up_member_name = self.nan_if_nat(
                data["NOMBRE DEL INTEGRANTE DE UP"][i]
            )
            data_up_member_dni = self.zero_if_nan(self.nan_if_nat(data["N° DNI.1"][i]))
            data_up_member_sex = self.nan_if_nat(data["SEXO IUP"][i])
            data_anual_utm_coordinates = self.nan_if_nat(
                data["COORDENADAS UTM ANUALES"][i]
            )
            data_producer_classification = self.nan_if_nat(
                data["TIPIFICACION DE PRODUCTORES (A-B-C)"][i]
            )
            data_employ_responsable = self.nan_if_nat(data["NOMBRE DE RESPONSABLE"][i])
            data_employ_specialist = self.nan_if_nat(
                data["NOMBRE DE RESPONSABLE DE ACTIVIDAD"][i]
            )
            data_activity = self.nan_if_nat(data["ACTIVIDAD REALIZADA"][i])
            #
            data_planting_intention_hectares = self.zero_if_nan(
                data["HAS. INTENS. DE SIEMBRA"][i]
            )
            data_ground_analysis = self.zero_if_nan(data["ANAL. SUELO"][i])
            data_plow_hours = self.zero_if_nan(data["HORAS ARADO"][i])
            data_dredge_hours = self.zero_if_nan(data["HORAS RASTRA"][i])
            data_oat_kg = self.zero_if_nan(data["KG AVENA"][i])
            data_vicia_kg = self.zero_if_nan(data["KG VICIA"][i])
            data_alfalfa_kg = self.zero_if_nan(data["KG ALFALFA"][i])
            data_dactylis_kg = self.zero_if_nan(data["KG DACTYLIS"][i])
            data_ryegrass_kg = self.zero_if_nan(data["KG RYEGRASS"][i])
            data_trebol_b_kg = self.zero_if_nan(data["KG TREBOL"][i])
            data_fertilizer = self.zero_if_nan(data["FERTILIZANTE (BOLSAS X 50 KG)"][i])
            data_avena_vicia_planted_hectares = self.zero_if_nan(
                data["HAS. SIEMBRA AVENA/VICIA"][i]
            )
            data_alfalfa_dactylis_planted_hectares = self.zero_if_nan(
                data["HAS. SIEMBRA ALFALFA DACTYLIS"][i]
            )
            data_ryegrass_trebol_planted_hectares = self.zero_if_nan(
                data["HAS. SIEMBRA RYEGRASS TREBOL"][i]
            )
            data_direct_grazing = self.zero_if_nan(data["PASTOREO DIRECTO (%)"][i])
            data_hay = self.zero_if_nan(data["HENO (%)"][i])
            data_ensilage = self.zero_if_nan(data["ENSILADO (%)"][i])
            data_bale = self.zero_if_nan(data["PACAS (%)"][i])
            data_perennial_grazing = self.zero_if_nan(data["PASTOREO % PERENNE"][i])
            data_perennial_ensilage = self.zero_if_nan(data["ENSILADO % PERENNE"][i])
            data_perennial_yield = self.zero_if_nan(data["RENDIMIENTO PERENNE"][i])
            data_anual_yield = self.zero_if_nan(data["RENDIMIENTO ANUALES KG MV/HA"][i])
            data_technical_assistance = self.zero_if_nan(data["ASISTENCIA TECNICA"][i])
            data_technical_training_perennial = self.zero_if_nan(
                data["CAPACITACION INSTALACION PERENNES"][i]
            )
            data_technical_training_anual = self.zero_if_nan(
                data["CAPACITACION INSTALACION ANUALES"][i]
            )
            data_technical_training_conservation = self.zero_if_nan(
                data["CAPACITACION MANEJO Y CONSERVACION"][i]
            )

            mapping_activity_detail = {
                "planting_intention_hectares": data_planting_intention_hectares,
                "ground_analysis": data_ground_analysis,  # falta asignar a una actividad
                "plow_hours": data_plow_hours,  #
                "dredge_hours": data_dredge_hours,  #
                "oat_kg": data_oat_kg,
                "vicia_kg": data_vicia_kg,
                "alfalfa_kg": data_alfalfa_kg,
                "dactylis_kg": data_dactylis_kg,
                "ryegrass_kg": data_ryegrass_kg,
                "trebol_b_kg": data_trebol_b_kg,
                "fertilizer": data_fertilizer,
                "avena_vicia_planted_hectares": data_avena_vicia_planted_hectares,
                "alfalfa_dactylis_planted_hectares": data_alfalfa_dactylis_planted_hectares,
                "ryegrass_trebol_planted_hectares": data_ryegrass_trebol_planted_hectares,
                "technical_assistance": data_technical_assistance,
                "anual_yield": data_anual_yield,
                "direct_grazing": data_direct_grazing,
                "hay": data_hay,
                "ensilage": data_ensilage,
                "bale": data_bale,
                "perennial_grazing": data_perennial_grazing,
                "perennial_ensilage": data_perennial_ensilage,
                "perennial_yield": data_perennial_yield,
                "technical_training_perennial": data_technical_training_perennial,
                "technical_training_anual": data_technical_training_anual,
                "technical_training_conservation": data_technical_training_conservation,
            }

            try:
                employ_responsable = self.get_person(data_employ_responsable)
                employ_specialist = self.get_person(data_employ_specialist)
                activity = self.get_activity(
                    data_activity.upper(), creates_if_none=False
                )
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
                quantity_value = 0
                activity_field_for_quantity = mapping_activity_quantity.get(
                    data_activity.lower()
                )
                if not isinstance(activity_field_for_quantity, list):
                    quantity_value = mapping_activity_detail.get(
                        activity_field_for_quantity
                    )
                else:
                    quantity_value = sum(activity_field_for_quantity)

                visits.append(
                    VisitGrass(
                        visited_at=data_visited_at,
                        production_unit=production_unit,
                        utm_coordenate=data_anual_utm_coordinates,
                        producer_classification=data_producer_classification,
                        employ_specialist=employ_specialist,
                        employ_responsable=employ_responsable,
                        activity=activity,
                        quantity=quantity_value,
                        hay=data_hay,
                        ensilage=data_ensilage,
                        bale=data_bale,
                        perennial_grazing=data_perennial_grazing,
                        perennial_ensilage=data_perennial_ensilage,
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
