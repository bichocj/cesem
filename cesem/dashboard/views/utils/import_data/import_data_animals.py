import os
from django.conf import settings
from core.models import (
    Activity,
    Community,
    Diagnostic,
    Drug,
    SicknessObservation,
    Zone,
    VisitAnimal,
    Sector,
)
import pandas as pd

from .utils import HelperImport

baset_path = os.path.join(settings.BASE_DIR, "core", "management", "commands", "files")


class ImportAnimals(HelperImport):
    help = "import xls data"
    diagnostic_names = {}
    sickness_observation_names = {}

    def __init__(self):
        super().__init__()
        diagnostics = Diagnostic.objects.all()
        for d in diagnostics:
            self.diagnostic_names[d.name] = d

        sickness_observations = SicknessObservation.objects.all()
        for s in sickness_observations:
            self.sickness_observation_names[s.name] = s

        self.columns_names = [
            "Nº",
            "MES",
            "FECHA",
            "ZONA",
            "COMUNIDAD ",
            "PDE-2019",
            "SECTOR/IRRIGACION DE LA UP ",
            "TIPOLOGIA DE UP",
            "UP ES PILOTO?",
            "NOMBRE RESPONSABLE UP",
            "Nº DNI",
            "SEXO RUP",
            "NOMBRE DEL INTEGRANTE DE LA UP",
            "Nº DNI.1",
            "SEXO IUP",
            "SECTOR/IRRIGACION DEL BENEFICIARIO",
            "NOMBRE DE ESPECIALISTA",
            "RESPONSABLE DE ACTIVIDAD",
            "ACTIVIDAD REALIZADA",
            "SECCION 1",
            "ENFERMEDAD/TRANSTORNO/OBSERVACION",
            "DIAGNOSTICO",
            "VACA",
            "VAQUILLONA",
            "VAQUILLA",
            "TERNERO",
            "TORETE",
            "TORO",
            "VACUNOS",
            "OVINOS",
            "ALPACAS",
            "LLAMAS",
            "CANES",
            "1 FARMACOS /SALES",
            "CANTIDAD",
            "U.M.",
            "2 FARMACOS /SALES",
            "CANTIDAD.1",
            "U.M..1",
            "3 FARMACOS /SALES",
            "CANTIDAD.2",
            "U.M..2",
            "4 FARMACOS /SALES",
            "CANTIDAD.3",
            "U.M..3",
        ]

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

    def zero_if_nan(self, val):
        try:
            if str(float(val)).lower() == "nan":
                return 0
        except:
            return 0
        # if math.isnan(val):
        return val

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
        df = pd.read_excel(file)
        self.validate_file(df, filename=file._name)
        print("start validate")
        self.validate_columns(df)
        print("validated")

        data = df.to_dict()
        rows_count = len(data["Nº"].keys())
        visits = []

        for i in range(rows_count):
            # data['Nº'][i]
            # data['MES'][i]
            data_visited_at = self.none_if_nat(data["FECHA"][i])
            data_zone = self.nan_if_nat(data["ZONA"][i])
            data_community = self.nan_if_nat(data["COMUNIDAD "][i])
            # data['PDE-2019'][i]
            data_sector = self.nan_if_nat(data["SECTOR/IRRIGACION DE LA UP "][i])
            data_tipology = self.nan_if_nat(data["TIPOLOGIA DE UP"][i])
            data_is_pilot = self.nan_if_nat(data["UP ES PILOTO?"][i]) == "SI"
            data_up_responsable_name = self.nan_if_nat(data["NOMBRE RESPONSABLE UP"][i])
            data_up_responsable_dni = self.nan_if_nat(data["Nº DNI"][i])
            try:
                data_up_responsable_dni = int(data_up_responsable_dni)
            except:
                pass

            data_up_responsable_sex = self.nan_if_nat(data["SEXO RUP"][i])
            data_up_member_name = self.nan_if_nat(
                data["NOMBRE DEL INTEGRANTE DE LA UP"][i]
            )
            data_up_member_dni = self.nan_if_nat(data["Nº DNI.1"][i])
            data_up_member_sex = self.nan_if_nat(data["SEXO IUP"][i])
            # data['SECTOR/IRRIGACION DEL BENEFICIARIO'][i]
            data_employ_specialist = self.nan_if_nat(data["NOMBRE DE ESPECIALISTA"][i])
            data_employ_responsable = self.nan_if_nat(
                data["RESPONSABLE DE ACTIVIDAD"][i]
            )
            data_activity = self.nan_if_nat(data["ACTIVIDAD REALIZADA"][i])
            # data['SECCION 1'][i]
            data_sickness_observation = self.nan_if_nat(
                data["ENFERMEDAD/TRANSTORNO/OBSERVACION"][i]
            )
            data_diagnostic = self.nan_if_nat(data["DIAGNOSTICO"][i])
            data_vaca = data["VACA"][i]
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
            data_ovinos = self.zero_if_nan(data["OVINOS"][i])
            data_alpacas = self.zero_if_nan(data["ALPACAS"][i])
            data_llamas = self.zero_if_nan(data["LLAMAS"][i])
            data_canes = self.zero_if_nan(data["CANES"][i])
            # data['1 FARMACOS /SALES'][i]
            # data['CANTIDAD'][i]
            # data['U.M.'][i]
            # data['2 FARMACOS /SALES'][i]
            # data['CANTIDAD.1'][i]
            # data['U.M..1'][i]
            # data['3 FARMACOS /SALES'][i]
            # data['CANTIDAD.2'][i]
            # data['U.M..2'][i]
            # data['4 FARMACOS /SALES'][i]
            # data['CANTIDAD.3'][i]
            # data['U.M..3'][i]

            try:
                employ_specialist = self.get_person(data_employ_specialist)
                employ_responsable = self.get_person(data_employ_responsable)
                activity = self.get_activity(data_activity, creates_if_none)
                sickness_observation = self.get_sickness_observation(
                    data_sickness_observation, creates_if_none
                )
                diagnostic = self.get_diagnostic(data_diagnostic, creates_if_none)
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
                    data_is_pilot=data_is_pilot,
                    data_tipology=data_tipology,
                    creates_if_none=creates_if_none,
                )

                visits.append(
                    VisitAnimal(
                        visited_at=data_visited_at,
                        production_unit=production_unit,
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
                    )
                )
                print("Registrando visita de animales Nº: ", i + 1)

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
            except Diagnostic.DoesNotExist:
                print("row", str(i + 1), "not found diagnostic:", data_diagnostic)
                exit()
            except SicknessObservation.DoesNotExist:
                print(
                    "row",
                    str(i + 1),
                    "not found sickness/observation:",
                    data_sickness_observation,
                )
                exit()

        VisitAnimal.objects.bulk_create(visits)
        return len(visits)
