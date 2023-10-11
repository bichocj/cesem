import pandas as pd
import hashlib
from core.models import (
    Person,
    Zone,
    Activity,
    Community,
    Sector,
    ProductionUnit,
    FilesChecksum,
)


class HelperImport:
    columns_names = []
    people_names = {}
    zones_names = {}
    activities_names = {}
    community_names = {}
    sector_names = {}

    def __init__(self):
        people = Person.objects.all()
        for p in people:
            self.people_names[p.name] = p

        zones = Zone.objects.all()
        for z in zones:
            self.zones_names[z.name] = z

        activities = Activity.objects.all()
        for a in activities:
            self.activities_names[a.short_name or a.name] = a

        communities = Community.objects.all()
        for c in communities:
            self.community_names[c.name] = c

        sectors = Sector.objects.all()
        for s in sectors:
            self.sector_names[s.name] = s

    def add_arguments(self, parser):
        parser.add_argument(
            "--creates_if_none",
            default=False,
            help="it creates activites, diagnostics and sickness if doesnt exists",
        )

    def zero_if_nan(self, val, to_int=False):
        try:
            if str(float(val)).lower() == "nan":
                return 0
        except:
            return 0

        if to_int:
            try:
                return int(val)
            except:
                return 0
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

    def none_if_nan(self, val):
        if val == "nan":
            return None

    def get_person(self, name, dni=None, sex=None):
        sex_data = None
        name = str(name)
        if sex == "M":
            sex_data = Person.Sexs.MALE
        if sex == "F":
            sex_data = Person.Sexs.FEMALE

        person = None
        if name in self.people_names:
            person = self.people_names[name]
        else:
            try:
                person = Person.objects.get(name=name)
            except Person.DoesNotExist:
                person = Person.objects.create(name=name, dni=dni, sex=sex_data)
                self.people_names[name] = person
        return person

    def get_zone(self, name, creates_if_none):
        zone = None
        name = str(name)
        if name in self.zones_names:
            zone = self.zones_names[str(name)]
        else:
            if creates_if_none:
                zone = Zone.objects.create(name=name)
                self.zones_names[str(name)] = zone
            else:
                raise Zone.DoesNotExist()
        return zone

    def get_community(self, name, zone, creates_if_none):
        community = None
        name = str(name)
        if name in self.community_names:
            community = self.community_names[name]
        else:
            if creates_if_none:
                community = Community.objects.create(name=name, zone=zone)
                self.community_names[name] = community
            else:
                raise Community.DoesNotExist()
        return community

    def get_sector(self, name, community, creates_if_none):
        sector = None
        name = str(name)
        if name in self.sector_names:
            sector = self.sector_names[name]
        else:
            if creates_if_none:
                sector = Sector.objects.create(name=name, community=community)
                self.sector_names[name] = sector
            else:
                raise Sector.DoesNotExist()
        return sector

    def get_activity(self, name, creates_if_none):
        activity = None
        name = str(name)
        if name in self.activities_names:
            activity = self.activities_names[name]
        else:
            if creates_if_none:
                activity = Activity.objects.create(name=name, short_name=name)
                self.activities_names[name] = activity
            else:
                raise Activity.DoesNotExist()
        return activity

    def get_production_unit(
        self,
        data_zone,
        data_community,
        data_sector,
        data_up_responsable_name,
        data_up_responsable_dni,
        data_up_responsable_sex,
        data_up_member_name,
        data_up_member_dni,
        data_up_member_sex,
        data_tipology=0,
        data_is_pilot=False,
        creates_if_none=False,
    ):
        zone = self.get_zone(data_zone, creates_if_none)
        community = self.get_community(data_community, zone, creates_if_none)
        sector = self.get_sector(data_sector, community, creates_if_none)
        up_responsable = self.get_person(
            data_up_responsable_name, data_up_responsable_dni, data_up_responsable_sex
        )
        up_member = self.get_person(
            data_up_member_name, data_up_member_dni, data_up_member_sex
        )

        production_unit, created = ProductionUnit.objects.get_or_create(
            zone=zone,
            community=community,
            sector=sector,
            person_responsable=up_responsable,
            person_member=up_member,
        )

        if created:
            if (
                production_unit.tipology != data_tipology
                or production_unit.is_pilot != data_is_pilot
            ):
                production_unit.tipology = data_tipology
                production_unit.is_pilot = data_is_pilot
                production_unit.save()

        return production_unit

    def validate_file(self, df):
        checksum = hashlib.sha256(df.to_json().encode()).hexdigest()
        try:
            FilesChecksum.objects.get(checksum=checksum)
            message = "Parece que este archivo ya fue subido anteriormente"
            raise Exception(message)
        except FilesChecksum.DoesNotExist:
            pass
        return checksum

    def create_checksum(self, df, filename, visits):
        checksum = hashlib.sha256(df.to_json().encode()).hexdigest()
        FilesChecksum.objects.create(checksum=checksum, filename=filename, visits=visits)

    def validate_columns(self, df):
        columns_xls = df.columns.ravel()
        columns_missing = []
        for column_name in self.columns_names:
            if column_name not in columns_xls:
                columns_missing.append(column_name)

        if len(columns_missing) > 0:
            message = "El archivo subido no tiene las siguientes columnas: {}".format(
                ",".join(columns_missing)
            )
            raise Exception(message)

    def execute(self, file, creates_if_none=True):
        # Here validate the file checksum and columns
        df = pd.read_excel(file)
        checksum = self.validate_file(df)
        # self.validate_columns(df)

        # Here run the implemented _inner_execute func in child class
        return_value = self._inner_execute(file, creates_if_none, checksum)

        # After save all data let's create a checksum to avoid process a file that already uploaded before
        self.create_checksum(df, filename=file._name, visits=return_value)
        return return_value

    def _inner_execute(self, file, creates_if_none, checksum):
        return 0
