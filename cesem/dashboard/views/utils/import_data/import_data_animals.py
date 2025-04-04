import os
from datetime import datetime
from django.conf import settings
from core.models import (
    Activity,
    Community,
    Diagnostic,
    Drug,
    SicknessObservation,
    Zone,
    VisitAnimalHealth,
    VisitAnimalHealthDetails,
    VisitAnimalDeworming,
    Sector,
    VisitGeneticImprovementVacuno,
    VisitGeneticImprovementOvino,
    VisitGeneticImprovementAlpaca,
    ImportIn
)
import pandas as pd
from .utils import HelperImport
import logging

logger = logging.getLogger(__name__)

baset_path = os.path.join(settings.BASE_DIR, "core", "management", "commands", "files")


class ImportAnimals(HelperImport):
    help = "import xls data"
    diagnostic_names = {}
    sickness_observation_names = {}
    drugs_names = {}
    dewormed_activities = [
        "desparasitación interna",
    ]
    sales_activities = [
        "campaña de entrega de sales minerales",
    ]
    vacuno_activities = [
        "inseminación artificial en ganado vacuno de leche",
        "capacitación en manejo reproductivo de ganado vacuno lechero",
        "asistencia técnica en manejo de ganado vacuno lechero",
        "evaluación y diagnóstico de vacas preñadas",
        "registro de crías nacidas de vacuno",
        "evaluación de vacas con problemas reproductivos",
        "seguimiento de vacas con problemas reproductivos",
        "sincronización de celo",
    ]
    ovino_activities = [
        "inseminación artificial de ovinos",
        "selección, identificación y preparación de ovinos para ia",
        "curso taller en manejo de ovinos",
        "asistencia técnica en producción de ganado ovino corriedale",
        "evaluación y diagnóstico de borregas inseminadas",
        "sincronización de celo de ovinos para ia",
        "registro de crías nacidas de ovino",
        "actividades complementarias",
    ]
    alpaca_activities = [
        "empadre controlado de alpacas",
        "selección de alpacas para empadre controlado",
        "curso taller en selección de reproductores y manejo de alpacas",
        "asistencia técnica en buenas prácticas de manejo de alpacas",
        "caracterización fenotípica de hatos alpaqueros",
        "evaluación y diagnóstico de alpacas preñadas",
        "evaluación de progenie de alpacas huacaya y suri",
    ]

    def __init__(self):
        super().__init__()
        diagnostics = Diagnostic.objects.all()
        for d in diagnostics:
            self.diagnostic_names[d.name] = d

        sickness_observations = SicknessObservation.objects.all()
        for s in sickness_observations:
            self.sickness_observation_names[s.name] = s

        drugs = Drug.objects.all()
        for s in drugs:
            self.drugs_names[s.name] = s

        self.columns_names = [
            "N",
            "MES",
            "FECHA",
            "ZONA",
            "COMUNIDAD",
            "PDE-2019",
            "SECTOR/IRRIGACION",
            "TIPOLOGIA DE UP",
            "UP ES PILOTO?",
            "NOMBRE RESPONSABLE UP",
            "N DNI",
            "SEXO RUP",
            "NOMBRE DEL INTEGRANTE DE UP",
            "N DNI.1",
            "SEXO IUP",
            "NOMBRE DE ESPECIALISTA",
            "NOMBRE DE RESPONSABLE DE ACTIVIDAD",
            "ACTIVIDAD REALIZADA",
        ]
        
        activities = Activity.objects.filter(import_in__isnull=False)
        for a in activities:
            if a.import_in == ImportIn.DEWORMING:
                self.dewormed_activities.append(a.name.lower())
            if a.import_in == ImportIn.SALES:
                self.sales_activities.append(a.name.lower())
            if a.import_in == ImportIn.VACUNO:
                self.vacuno_activities.append(a.name.lower())
            if a.import_in == ImportIn.OVINO:
                self.ovino_activities.append(a.name.lower())
            if a.import_in == ImportIn.ALPACA:
                self.alpaca_activities.append(a.name.lower())


    def get_diagnostic(self, name, creates_if_none):
        diagnostic = None
        if name in self.diagnostic_names:
            diagnostic = self.diagnostic_names[name]
        else:
            if creates_if_none:
                diagnostic = Diagnostic.objects.create(name=name)
                self.diagnostic_names[name] = diagnostic
            else:
                raise Diagnostic.DoesNotExist()
        return diagnostic

    def get_sickness_observation(self, name, creates_if_none):
        sickness_observation = None
        if name in self.sickness_observation_names:
            sickness_observation = self.sickness_observation_names[name]
        else:
            if creates_if_none:
                sickness_observation = SicknessObservation.objects.create(name=name)
                self.sickness_observation_names[name] = sickness_observation
            else:
                raise SicknessObservation.DoesNotExist()
        return sickness_observation

    def get_drug(self, name, um, creates_if_none):
        drug = None
        if name in self.drugs_names:
            drug = self.drugs_names[name]
        else:
            if creates_if_none:
                drug = Drug.objects.create(name=name, um=um)
                self.drugs_names[name] = drug
            else:
                raise Drug.DoesNotExist()
        return drug

    def _inner_execute(self, file, creates_if_none=True, checksum=""):
        df = pd.read_excel(file)
        data = df.to_dict()
        rows_count = len(data["N"].keys())
        visits_animals = []
        visits_dewormed = []
        visits_ovinos = []
        visits_vacunos = []
        visits_alpacas = []
        visits_details = []

        for i in range(rows_count):
            # data['N'][i]
            # data['MES'][i] ################
            data_visited_at = self.none_if_nat(data["FECHA"][i])
            data_visited_at = self.to_date(data_visited_at, i + 1)

            data_zone = self.nan_if_nat(data["ZONA"][i])
            data_community = self.nan_if_nat(data["COMUNIDAD"][i])
            # data['PDE-2019'][i]
            data_sector = self.nan_if_nat(data["SECTOR/IRRIGACION"][i])
            data_tipology = self.zero_if_nan(
                self.nan_if_nat(data["TIPOLOGIA DE UP"][i]), True
            )
            data_is_pilot = self.nan_if_nat(data["UP ES PILOTO?"][i]) == "SI"
            data_up_responsable_name = self.nan_if_nat(
                data["NOMBRE DEL RESPONSABLE UP"][i]
            )
            data_up_responsable_dni = self.zero_if_nan(data["N DNI"][i], to_int=True)
            data_up_responsable_sex = self.nan_if_nat(data["SEXO RUP"][i])
            data_up_member_name = self.nan_if_nat(
                data["NOMBRE DEL INTEGRANTE DE UP"][i]
            )
            data_up_member_dni = self.zero_if_nan(data["N DNI.1"][i], to_int=True)
            data_up_member_sex = self.get_sex(self.nan_if_nat(data["SEXO IUP"][i]))
            # data['SECTOR/IRRIGACION DEL BENEFICIARIO'][i]
            data_employ_specialist = self.nan_if_nat(data["NOMBRE DE ESPECIALISTA"][i])
            data_employ_responsable = self.nan_if_nat(
                data["NOMBRE DE RESPONSABLE DE ACTIVIDAD"][i]
            )
            data_activity = self.nan_if_nat(data["ACTIVIDAD REALIZADA"][i])

            try:
                employ_specialist = self.get_person(
                    data_employ_specialist, "NOMBRE DE ESPECIALISTA",  creates_if_none=False
                )
                employ_responsable = self.get_person(
                    data_employ_responsable, "NOMBRE DE RESPONSABLE DE ACTIVIDAD", creates_if_none=False
                )
                activity = self.get_activity(
                    data_activity, creates_if_none=False, row=i + 1
                )
                production_unit = self.get_production_unit(
                    data_zone,
                    data_community,
                    data_sector,
                    data_up_responsable_name,
                    data_up_responsable_dni,
                    data_up_responsable_sex,
                    data_is_pilot=data_is_pilot,
                    data_tipology=data_tipology,
                    row=i + 1,
                )

                if data_activity.lower() in self.vacuno_activities:
                    try:
                        # DATA OF "MEJORAMIENTO GENETICO"
                        data_bull_name = data["NOMBRE DE TORO"][i]
                        data_bull_race = data["RAZA DE TORO"][
                            i
                        ]  # solicitar cambio de nombre, nombre original:raza
                        data_pajilla_type = data["TIPO PAJILLA"][i]
                        data_pajilla_origin = data["PROCEDENCIA PAJILLA"][i]
                        data_pajillas_number = self.zero_if_nan(
                            data["N DE PAJILLAS"][i]
                        )

                        data_cow_name = data["NOMBRE DE VACA"][i]
                        data_cow_race = data["RAZA DE VACA"][i]
                        data_service_number = data["N DE SERVICIO"][
                            i
                        ]  # verificar caracter

                        data_pregnant_vacuno = self.zero_if_nan(data["PREÑADA"][i])
                        data_empty_vacuno = self.zero_if_nan(data["VACIA"][i])

                        data_birthday = data["F. NACIMIENTO"][i]
                        data_earring_number = data["N DE ARETE"][
                            i
                        ]  # verificar caracter
                        data_baby_name = data["NOMBRE DE CRIA"][i]
                        data_male = self.zero_if_nan(data["MACHO"][i])
                        data_female = self.zero_if_nan(data["HEMBRA"][i])
                        data_death = self.zero_if_nan(data["MUERTA"][i])
                        data_baby_bull_name = data["CRIA-NOMBRE DE TORO"][
                            i
                        ]  # solicitar cambio de nombre, nombre original: nombre de toro
                        data_baby_cow_name = data["CRIA-NOMBRE DE VACA"][
                            i
                        ]  # solicitar cambio de nombre, nombre original: nombre de vaca
                        data_male_attendance = self.zero_if_nan(
                            data["ASIS VARONES CAPAC MANEJO REPRODUCTIVO"][i]
                        )
                        data_female_attendance = self.zero_if_nan(
                            data["ASIS MUJERES CAPAC MANEJO REPRODUCTIVO"][i]
                        )
                        data_technical_assistance_attendance = self.zero_if_nan(
                            data["ASIS TEC MANEJO GANADO VACUNO"][i]
                        )
                        data_vaca = self.zero_if_nan(data["VACA"][i])
                        data_vaquillona = self.zero_if_nan(data["VAQUILLONA"][i])
                        data_vaquilla = self.zero_if_nan(data["VAQUILLA"][i])
                        data_terreno = self.zero_if_nan(data["TERNERO"][i])
                        data_torete = self.zero_if_nan(data["TORETE"][i])
                        data_toro = self.zero_if_nan(data["TORO"][i])
                        data_vacunos_number = (
                            data_vaca
                            + data_vaquillona
                            + data_vaquilla
                            + data_terreno
                            + data_torete
                            + data_toro
                        )

                        visit_vacuno = VisitGeneticImprovementVacuno(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            up_member_name=data_up_member_name,
                            up_member_dni=data_up_member_dni,
                            sex=data_up_member_sex,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=activity,
                            bull_name=data_bull_name,
                            bull_race=data_bull_race,
                            pajilla_type=data_pajilla_type,
                            pajilla_origin=data_pajilla_origin,
                            pajillas_number=data_pajillas_number,
                            cow_name=data_cow_name,
                            cow_race=data_cow_race,
                            service_number=data_service_number,
                            pregnant=data_pregnant_vacuno,
                            empty=data_empty_vacuno,
                            birthday=data_birthday,
                            earring_number=data_earring_number,
                            baby_name=data_baby_name,
                            male=data_male,
                            female=data_female,
                            death=data_death,
                            baby_bull_name=data_baby_bull_name,
                            baby_cow_name=data_baby_cow_name,
                            male_attendance=data_male_attendance,
                            female_attendance=data_female_attendance,
                            technical_assistance_attendance=data_technical_assistance_attendance,
                            vacunos_number=data_vacunos_number,
                            checksum=checksum,
                        )
                        visits_vacunos.append(visit_vacuno)
                    except Exception as e:
                        msg = (
                            "la actividad "
                            + str(data_activity)
                            + " requiere la columna "
                            + str(e)
                        )
                        raise ValueError(msg)

                elif data_activity.lower() in self.ovino_activities:
                    try:
                        data_course_male_attendance = self.zero_if_nan(
                            data["ASIS VARONES CURSO MANEJO OVINOS"][i]
                        )
                        data_course_female_attendance = self.zero_if_nan(
                            data["ASIS MUJERES CURSO MANEJO OVINOS"][i]
                        )
                        data_technical_assistance_attendance = self.zero_if_nan(
                            data["ASIS TEC PRODUCCION GANADO OVINO CORRIEDALE"][i]
                        )
                        data_selected_ovines = self.zero_if_nan(
                            data["OVINOS SELECCIONADOS"][i]
                        )
                        data_synchronized_ovines = self.zero_if_nan(
                            data["OVINOS SINCRONIZADOS"][i]
                        )
                        data_inseminated_sheeps_corriedale = self.zero_if_nan(
                            data["OVEJAS INSEMINADAS CORRIEDALE"][i]
                        )
                        data_inseminated_sheeps_criollas = self.zero_if_nan(
                            data["OVEJAS INSEMINADAS CRIOLLAS"][i]
                        )
                        data_pregnant_ovino = self.zero_if_nan(data["PREÑADA"][i])
                        data_empty_ovino = self.zero_if_nan(data["VACIA"][i])
                        data_not_evaluated = self.zero_if_nan(data["NO EVALUADA"][i])
                        data_baby_males = self.zero_if_nan(data["CRIA MACHO"][i])
                        data_baby_females = self.zero_if_nan(data["CRIA HEMBRA"][i])
                        data_baby_deaths = self.zero_if_nan(data["CRIA MUERTA"][i])
                        data_rgc_number = data["N RGC"][i]
                        data_ovinos_number = self.zero_if_nan(data["OVINOS"][i])
                        visit_ovino = VisitGeneticImprovementOvino(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            up_member_name=data_up_member_name,
                            up_member_dni=data_up_member_dni,
                            sex=data_up_member_sex,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=activity,
                            course_male_attendance=data_course_male_attendance,
                            course_female_attendance=data_course_female_attendance,
                            technical_assistance_attendance=data_technical_assistance_attendance,
                            selected_ovines=data_selected_ovines,
                            synchronized_ovines=data_synchronized_ovines,
                            inseminated_sheeps_corriedale=data_inseminated_sheeps_corriedale,
                            inseminated_sheeps_criollas=data_inseminated_sheeps_criollas,
                            pregnant=data_pregnant_ovino,
                            empty=data_empty_ovino,
                            not_evaluated=data_not_evaluated,
                            baby_males=data_baby_males,
                            baby_females=data_baby_females,
                            baby_deaths=data_baby_deaths,
                            ovinos_number=data_ovinos_number,
                            rgc_number=data_rgc_number,
                            checksum=checksum,
                        )
                        visits_ovinos.append(visit_ovino)
                        logger.info(
                            "Registrando visita de animales N:"
                            + str(i + 1)
                            + ", TIPO: MG ovino"
                        )
                    except Exception as e:
                        msg = (
                            "la actividad "
                            + data_activity
                            + " requiere la columna "
                            + str(e)
                        )
                        raise ValueError(msg)

                elif data_activity.lower() in self.alpaca_activities:
                    try:
                        data_hato_number = self.zero_if_nan(data["N DE HATO"][i])
                        data_hato_babies_number = self.zero_if_nan(
                            data["N DE CRIAS EN HATO"][i]
                        )
                        data_hato_mothers_number = self.zero_if_nan(
                            data["N DE MADRES EN HATO"][i]
                        )
                        data_hato_males_number = self.zero_if_nan(
                            data["N DE MACHOS EN HATO"][i]
                        )
                        data_female_alpaca_earring_number = data[
                            "SELEC N ARETE ALPACA HEMBRA"
                        ][i]
                        data_female_alpaca_race = data["SELEC RAZA ALPACA HEMBRA"][i]
                        data_female_alpaca_color = data["SELEC COLOR ALPACA HEMBRA"][i]
                        data_female_alpaca_age = data["SELEC EDAD ALPACA HEMBRA"][i]
                        data_female_alpaca_category = data[
                            "SELEC CATEGORIA ALPACA HEMBRA"
                        ][i]
                        data_female_alpaca_total_score = self.zero_if_nan(
                            data["SELEC PUNTAJE TOTAL ALPACA HEMBRA"][i]
                        )
                        data_selected_alpacas_number = self.zero_if_nan(
                            data["SELEC CANT ALPACAS SELECCIONADAS"][i]
                        )
                        data_empadre_date = self.none_if_nan(
                            self.none_if_nat(data["FECHA EMPADRE"][i])
                        )
                        data_alpacas_empadradas = data["ALPACAS EMPADRADAS"][i]
                        data_alpacas_empadradas_number = self.zero_if_nan(
                            data["N DE ALPACAS EMPADRADAS"][i]
                        )
                        data_male_empadre_number = data["N MACHO EMPADRE"][i]
                        data_second_service_date = self.none_if_nan(
                            self.none_if_nat(data["FECHA 2DO SERVICIO"][i])
                        )
                        data_second_service_male_number = data["N MACHO 2DO SERVICIO"][
                            i
                        ]
                        data_pregnant_alpaca = self.zero_if_nan(data["PREÑADA"][i])
                        data_empty_alpaca = self.zero_if_nan(data["VACIA"][i])
                        data_baby_birthday = self.none_if_nan(
                            self.none_if_nat(data["F. NACIMIENTO CRIA"][i])
                        )
                        data_baby_earring_number = data["N ARETE CRIA"][i]
                        data_female_baby = self.zero_if_nan(data["CRIA HEMBRA"][i])
                        data_male_baby = self.zero_if_nan(data["CRIA MACHO"][i])
                        data_mortality_baby = self.zero_if_nan(
                            data["MORTANDAD CRIA"][i]
                        )
                        data_mother_of_baby = data["MADRE DE CRIA"][i]
                        data_father_of_baby = data["PADRE DE CRIA"][i]
                        data_training_male_attendance = self.zero_if_nan(
                            data["ASIS VARONES CAPAC"][i]
                        )
                        data_training_female_attendance = self.zero_if_nan(
                            data["ASIS MUJERES CAPAC"][i]
                        )
                        data_technical_assistance_attendance = self.zero_if_nan(
                            data["ASIS TEC BUENAS PRACTICAS MANEJO ALPACAS"][i]
                        )

                        visit_alpaca = VisitGeneticImprovementAlpaca(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            up_member_name=data_up_member_name,
                            up_member_dni=data_up_member_dni,
                            sex=data_up_member_sex,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=activity,
                            hato_number=data_hato_number,
                            hato_babies_number=data_hato_babies_number,
                            hato_mothers_number=data_hato_mothers_number,
                            hato_males_number=data_hato_males_number,
                            female_alpaca_earring_number=data_female_alpaca_earring_number,
                            female_alpaca_race=data_female_alpaca_race,
                            female_alpaca_color=data_female_alpaca_color,
                            female_alpaca_age=data_female_alpaca_age,
                            female_alpaca_category=data_female_alpaca_category,
                            female_alpaca_total_score=data_female_alpaca_total_score,
                            selected_alpacas_number=data_selected_alpacas_number,
                            empadre_date=data_empadre_date,
                            alpacas_empadradas=data_alpacas_empadradas,
                            alpacas_empadradas_number=data_alpacas_empadradas_number,
                            male_empadre_number=data_male_empadre_number,
                            second_service_date=data_second_service_date,
                            second_service_male_number=data_second_service_male_number,
                            pregnant=data_pregnant_alpaca,
                            empty=data_empty_alpaca,
                            baby_birthday=data_baby_birthday,
                            baby_earring_number=data_baby_earring_number,
                            female_baby=data_female_baby,
                            male_baby=data_male_baby,
                            mortality_baby=data_mortality_baby,
                            mother_of_baby=data_mother_of_baby,
                            father_of_baby=data_father_of_baby,
                            training_male_attendance=data_training_male_attendance,
                            training_female_attendance=data_training_female_attendance,
                            technical_assistance_attendance=data_technical_assistance_attendance,
                            checksum=checksum,
                        )
                        visits_alpacas.append(visit_alpaca)
                        logger.info(
                            "Registrando visita de animales N:"
                            + str(i + 1)
                            + ", TIPO: MG alpaca"
                        )
                    except Exception as e:
                        msg = (
                            "la actividad "
                            + str(data_activity)
                            + " requiere la columna "
                            + str(e)
                        )
                        raise ValueError(msg)

                elif data_activity.lower() in self.dewormed_activities:
                    try:
                        data_v_race = data["VACUNOS RAZA"][i]
                        data_sickness_observation = self.nan_if_nat(
                            data["ENFERMEDAD/TRANSTORNO/OBSERVACION"][i]
                        )
                        data_diagnostic = self.nan_if_nat(data["DIAGNOSTICO"][i])
                        data_v_dewormed = self.zero_if_nan(
                            data["VACUNOS DESPARASITADOS"][i]
                        )
                        data_v_no_dewormed = self.zero_if_nan(
                            data["VACUNOS NO DESPARASITADOS"][i]
                        )
                        data_v_total = self.zero_if_nan(data["TOTAL VACUNOS"][i])
                        data_o_race = data["OVINOS RAZA"][i]
                        data_o_dewormed = self.zero_if_nan(
                            data["OVINOS DESPARASITADOS"][i]
                        )
                        data_o_no_dewormed = self.zero_if_nan(
                            data["OVINOS NO DESPARASITADOS"][i]
                        )
                        data_o_total = self.zero_if_nan(data["TOTAL OVINOS"][i])
                        data_a_race = data["ALPACAS RAZA"][i]
                        data_a_dewormed = self.zero_if_nan(
                            data["ALPACAS DESPARASITADOS"][i]
                        )
                        data_a_no_dewormed = self.zero_if_nan(
                            data["ALPACAS NO DESPARASITADOS"][i]
                        )
                        data_a_total = self.zero_if_nan(data["TOTAL ALPACAS"][i])
                        data_l_race = data["LLAMAS RAZA"][i]
                        data_l_dewormed = self.zero_if_nan(
                            data["LLAMAS DESPARASITADOS"][i]
                        )
                        data_l_no_dewormed = self.zero_if_nan(
                            data["LLAMAS NO DESPARASITADOS"][i]
                        )
                        data_l_total = self.zero_if_nan(data["TOTAL LLAMAS"][i])
                        data_c_total = self.zero_if_nan(data["CANES DESPARACITADOS"][i])
                        
                        data_total = data_v_total + data_o_total + data_a_total + data_l_total + data_c_total


                        visit_dewormed = VisitAnimalDeworming(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            up_member_name=data_up_member_name,
                            up_member_dni=data_up_member_dni,
                            sex=data_up_member_sex,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=activity,
                            sickness_observation=self.get_sickness_observation(
                                data_sickness_observation, creates_if_none
                            ),
                            diagnostic=self.get_diagnostic(
                                data_diagnostic, creates_if_none
                            ),
                            v_race=data_v_race,
                            v_dewormed=data_v_dewormed,
                            v_no_dewormed=data_v_no_dewormed,
                            v_total=data_v_total,
                            o_race=data_o_race,
                            o_dewormed=data_o_dewormed,
                            o_no_dewormed=data_o_no_dewormed,
                            o_total=data_o_total,
                            a_race=data_a_race,
                            a_dewormed=data_a_dewormed,
                            a_no_dewormed=data_a_no_dewormed,
                            a_total=data_a_total,
                            l_race=data_l_race,
                            l_dewormed=data_l_dewormed,
                            l_no_dewormed=data_l_no_dewormed,
                            l_total=data_l_total,
                            c_total=data_c_total,
                            total=data_total,
                            checksum=checksum,
                        )
                        visits_dewormed.append(visit_dewormed)
                    except Exception as e:
                        msg = (
                            "la actividad "
                            + str(data_activity)
                            + " requiere la columna "
                            + str(e)
                        )
                        raise ValueError(msg)
                elif data_activity.lower() in self.sales_activities:
                    try:
                        data_vacunos = self.zero_if_nan(data["VACUNOS"][i], to_int=True)
                        data_ovinos = self.zero_if_nan(data["OVINOS"][i], to_int=True)

                        data_sickness_observation = self.nan_if_nat(
                            data["ENFERMEDAD/TRANSTORNO/OBSERVACION"][i]
                        )
                        data_diagnostic = self.nan_if_nat(data["DIAGNOSTICO"][i])

                        sickness_observation = self.get_sickness_observation(
                            data_sickness_observation, creates_if_none
                        )
                        diagnostic = self.get_diagnostic(
                            data_diagnostic, creates_if_none
                        )

                        visit_animal = VisitAnimalHealth(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            up_member_name=data_up_member_name,
                            up_member_dni=data_up_member_dni,
                            sex=data_up_member_sex,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=activity,
                            sickness_observation=sickness_observation,
                            diagnostic=diagnostic,
                            ovinos=data_ovinos,
                            vacunos=data_vacunos,
                            checksum=checksum,
                            is_sal=True
                        )
                        visits_animals.append(visit_animal)
                        
                    except Exception as e:
                        msg = (
                            "la actividad "
                            + str(data_activity)
                            + " requiere la columna "
                            + str(e)
                        )
                        raise ValueError(msg)

                else:
                    try:
                        data_sickness_observation = self.nan_if_nat(
                            data["ENFERMEDAD/TRANSTORNO/OBSERVACION"][i]
                        )
                        data_diagnostic = self.nan_if_nat(data["DIAGNOSTICO"][i])
                        data_vaca = self.zero_if_nan(data["VACA"][i])
                        data_vaquillona = self.zero_if_nan(data["VAQUILLONA"][i])
                        data_vaquilla = self.zero_if_nan(data["VAQUILLA"][i])
                        data_terreno = self.zero_if_nan(data["TERNERO"][i])
                        data_torete = self.zero_if_nan(data["TORETE"][i])
                        data_toro = self.zero_if_nan(data["TORO"][i])
                        data_vacunos = (
                            data_vaca
                            + data_vaquillona
                            + data_vaquilla
                            + data_terreno
                            + data_torete
                            + data_toro
                        )
                        data_ovinos = self.zero_if_nan(data["OVINOS"][i], to_int=True)
                        data_alpacas = self.zero_if_nan(data["ALPACAS"][i], to_int=True)
                        data_llamas = self.zero_if_nan(data["LLAMAS"][i], to_int=True)
                        data_canes = self.zero_if_nan(data["CANES"][i], to_int=True)
                        data_medicine_name_1 = data["1 FARMACOS/SALES"][i]
                        data_um_name_1 = data["U.M."][i]
                        data_quantity_1 = self.zero_if_nan(
                            data["CANTIDAD"][i], to_int=True
                        )

                        data_medicine_name_2 = data["2 FARMACOS/SALES"][i]
                        data_um_name_2 = data["U.M..1"][i]
                        data_quantity_2 = self.zero_if_nan(
                            data["CANTIDAD.1"][i], to_int=True
                        )

                        data_medicine_name_3 = data["3 FARMACOS/SALES"][i]
                        data_um_name_3 = data["U.M..2"][i]
                        data_quantity_3 = self.zero_if_nan(
                            data["CANTIDAD.2"][i], to_int=True
                        )

                        data_medicine_name_4 = data["4 FARMACOS/SALES"][i]
                        data_um_name_4 = data["U.M..3"][i]
                        data_quantity_4 = self.zero_if_nan(
                            data["CANTIDAD.3"][i], to_int=True
                        )

                        sickness_observation = self.get_sickness_observation(
                            data_sickness_observation, creates_if_none
                        )
                        diagnostic = self.get_diagnostic(
                            data_diagnostic, creates_if_none
                        )

                        visit_animal = VisitAnimalHealth(
                            visited_at=data_visited_at,
                            production_unit=production_unit,
                            up_member_name=data_up_member_name,
                            up_member_dni=data_up_member_dni,
                            sex=data_up_member_sex,
                            employ_specialist=employ_specialist,
                            employ_responsable=employ_responsable,
                            activity=activity,
                            sickness_observation=sickness_observation,
                            diagnostic=diagnostic,
                            ovinos=data_ovinos,
                            alpacas=data_alpacas,
                            llamas=data_llamas,
                            canes=data_canes,
                            vaca=data_vaca,
                            vaquillona=data_vaquillona,
                            vaquilla=data_vaquilla,
                            terreno=data_terreno,
                            torete=data_torete,
                            toro=data_toro,
                            vacunos=data_vacunos,
                            checksum=checksum,
                        )
                        visits_animals.append(visit_animal)
                        logger.info(
                            "Registrando visita de animales N:"
                            + str(i + 1)
                            + ", sanidad animal"
                        )

                    except Exception as e:
                        msg = (
                            "la actividad "
                            + str(data_activity)
                            + " requiere la columna "
                            + str(e)
                        )
                        raise ValueError(msg)

                    if data_quantity_1 > 0:
                        drug = self.get_drug(
                            data_medicine_name_1, data_um_name_1, creates_if_none
                        )
                        visits_details.append(
                            VisitAnimalHealthDetails(
                                visit=visit_animal, drug=drug, quantity=data_quantity_1
                            )
                        )
                    if data_quantity_2 > 0:
                        drug = self.get_drug(
                            data_medicine_name_2, data_um_name_2, creates_if_none
                        )
                        visits_details.append(
                            VisitAnimalHealthDetails(
                                visit=visit_animal, drug=drug, quantity=data_quantity_2
                            )
                        )
                    if data_quantity_3 > 0:
                        drug = self.get_drug(
                            data_medicine_name_3, data_um_name_3, creates_if_none
                        )
                        visits_details.append(
                            VisitAnimalHealthDetails(
                                visit=visit_animal, drug=drug, quantity=data_quantity_3
                            )
                        )
                    if data_quantity_4 > 0:
                        drug = self.get_drug(
                            data_medicine_name_4, data_um_name_4, creates_if_none
                        )
                        visits_details.append(
                            VisitAnimalHealthDetails(
                                visit=visit_animal, drug=drug, quantity=data_quantity_4
                            )
                        )

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

        VisitAnimalHealth.objects.bulk_create(visits_animals)
        VisitAnimalHealthDetails.objects.bulk_create(visits_details)

        VisitAnimalDeworming.objects.bulk_create(visits_dewormed)
        VisitGeneticImprovementVacuno.objects.bulk_create(visits_vacunos)
        VisitGeneticImprovementOvino.objects.bulk_create(visits_ovinos)
        VisitGeneticImprovementAlpaca.objects.bulk_create(visits_alpacas)

        total = (
            len(visits_animals)
            + len(visits_vacunos)
            + len(visits_ovinos)
            + len(visits_alpacas)
            + len(visits_dewormed)
        )
        return total
