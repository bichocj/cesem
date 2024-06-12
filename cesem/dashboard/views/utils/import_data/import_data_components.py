import os
from django.conf import settings
from core.models import VisitComponents, Zone, Community, Activity, Sector
import pandas as pd

from .utils import HelperImport
import logging

baset_path = os.path.join(settings.BASE_DIR, "core", "management", "commands", "files")
logger = logging.getLogger(__name__)

mapping_activities = {
    "buenas prácticas de ordeño i": "2.1.1. BPO I",
    "buenas prácticas de ordeño ii": "2.1.2. BPO II",
    "producción de derivados lácteos": "2.1.3. PROD. DERV. LACTEOS",
    "como elaborar charqui": "2.2.1. ELAB. CHARQUI",
    "producción de carne de cordero para camal": "2.2.2. PROD. CARNE CORDERO CAMAL",
    "pre-esquila, esquila y cuidado de vellón": "2.3.1. PRE ESQ. ESQUILA VELLON",
    "manejo de registros de características genealógicas": "2.3.2. MANEJO DE REGISTRO DE C.G.",
    "desarrollo personal empresarial": "3.1.1. DES. PERS. EMPRESARIAL",
    "conociendo y organizando mi empresa": "3.1.2. CON. ORG. MI EMPRESA",
    "mercado y producto": "3.1.3. MERCADO Y PRODUCTO",
    "gestión de procesos": "3.1.4. GESTION DE PROCESOS",
    "gestión contable y tributaria": "3.1.5. GEST. TRIB. Y CONTABLE",
    "planificación estratégica": "3.1.6. PLAN. ESTRATEGICA",
    "plan de marketing": "3.1.7. PLAN DE MARKETING",
    "gestión y planificación financiera": "3.1.8. GEST. Y PLANF. FINANCIERA",
    "plan de gestión empresarial": "3.1.9. PLAN GEST. EMPRES",
    "pasantías a experiencias exitosas para conocimiento de mercado": "3.2.1. PASANT. EXPER. CONOC. MERCADO",
    "promover y fortalecer la participación en ferias comerciales locales y regionales": "3.2.2. FERIAS COMERCIALES REG. Y LOCALES",
    "fortalecer la participación de los productores en ferias comerciales": "3.2.3. FORTALECER LA PARTICIPACION FERIAS COMER.",
}


class ImportComponents(HelperImport):
    help = "import xls data"

    def __init__(self):
        super().__init__()
        self.columns_names = [
            "N PARTE",
            "AÑO",
            "FECHA",
            "DATOS GENERALES",
            "ZONA",
            "COMUNIDAD",
            "SECTOR/IRRIGACION",
            "NOMBRE RESPONSABLE UP",
            "N DNI",
            "SEXO RUP",
            "EDAD RUP",
            "TECNICO DE CADENAS",
            "ESPECIALISTA DE CADENAS",
            "CAPACITADOR(A)",
            "ACTIVIDAD REALIZADA",
        ]

    def _inner_execute(self, file, creates_if_none=True, checksum=""):
        df = pd.read_excel(file)
        data = df.to_dict()
        rows_count = len(data["N"].keys())
        visits = []
        for i in range(rows_count):
            data_parte_number = self.zero_if_nan(data["N PARTE"][i])
            data_year = data["AÑO"][i]
            data_visited_at = data["FECHA"][i]
            data_general_data = data["DATOS GENERALES"][i]
            data_zone = data["ZONA"][i]
            data_community = data["COMUNIDAD"][i]
            data_sector = data["SECTOR/IRRIGACION"][i]
            data_up_responsible_name = data["NOMBRE RESPONSABLE UP"][i]
            data_dni_responsible = data["N DNI"][i]
            data_gender_responsible = data["SEXO RUP"][i]
            data_age_responsible = self.zero_if_nan(data["EDAD RUP"][i])
            data_technical_employee = data["TECNICO DE CADENAS"][i]
            data_specialist_employee = data["ESPECIALISTA DE CADENAS"][i]
            data_trainer_employee = data["CAPACITADOR(A)"][i]
            data_activity = data["ACTIVIDAD REALIZADA"][i]
            data_certificate_delivery = self.zero_if_nan(
                data["ADICIONAL 01: ENTREGA DE CERTIFICADOS - GESTION EMPRESARIAL"][i]
            )
            data_pedagogical_process = self.zero_if_nan(
                data["ADICIONAL 02: PROCESOS PEDAGÓGICOS EQUIPO CESEM"][i]
            )

            data_quantity = self.zero_if_nan(
                data[mapping_activities.get(data_activity.lower())][i]
            )

            try:
                technical_employee = self.get_person(data_technical_employee, creates_if_none=False)
                specialist_employee = self.get_person(data_specialist_employee, creates_if_none=False)
                trainer_employee = self.get_person(data_trainer_employee, creates_if_none=False)
                activity = self.get_activity(
                    data_activity, creates_if_none=False, row=i + 1
                )
                production_unit = self.get_production_unit(
                    data_zone,
                    data_community,
                    data_sector,
                    data_up_responsible_name,
                    data_dni_responsible,
                    data_gender_responsible,
                    row=i + 1,
                    is_component=True,
                )

                visits.append(
                    VisitComponents(
                        parte_number=data_parte_number,
                        year=data_year,
                        visited_at=data_visited_at,
                        general_data=data_general_data,
                        production_unit=production_unit,
                        age=data_age_responsible,
                        technical_employee=technical_employee,
                        specialist_employee=specialist_employee,
                        trainer_employee=trainer_employee,
                        activity=activity,
                        quantity=data_quantity,
                        certificate_delivery=data_certificate_delivery,
                        pedagogical_process=data_pedagogical_process,
                    )
                )
                logger.info("Procesando registro de componentes Nº: " + str(i + 1))

            except Zone.DoesNotExist:
                msg = "fila " + str(i + 1) + " zona no encontrada:" + str(data_zone)
                raise ValueError(msg)
            except Community.DoesNotExist:
                msg = (
                    "fila "
                    + str(i + 1)
                    + " comunidad no encontrada:"
                    + str(data_community)
                )
                raise ValueError(msg)
            except Sector.DoesNotExist:
                msg = "fila " + str(i + 1) + " sector no encontrado:" + str(data_sector)
                raise ValueError(msg)
            except Activity.DoesNotExist:
                msg = (
                    "fila "
                    + str(i + 1)
                    + " actividad no encontrada: "
                    + str(data_activity)
                )
                raise ValueError(msg)
            except Exception as e:
                msg = "fila " + str(i + 1) + " " + str(e)
                raise ValueError(msg)
        VisitComponents.objects.bulk_create(visits)
        return len(visits)
