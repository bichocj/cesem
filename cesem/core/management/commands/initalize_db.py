import numbers
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import (
    Activity,
    Community,
    Diagnostic,
    Drug,
    SicknessObservation,
    Zone,
    Sector,
    Person,
)
import os

path = os.path.join(
    settings.BASE_DIR, "core", "management", "commands", "files", "initial_data.xls"
)


class Command(BaseCommand):
    help = "initialize db"

    def handle(self, *args, **options):
        df = pd.read_excel(path)
        data = df.to_dict()
        rows_count = len(data["N°"].keys())
        
        print("headers:")
        print(data.keys())
        print("")

        zones_count = Zone.objects.all().count()
        if zones_count > 0:
            print("There are a zone, we need an empty db for this action")
            exit()

        zones = {}
        for i in range(rows_count):            
            zone_name = data["ZONA"][i]
            if zone_name not in zones:
                zone = Zone.objects.create(name=zone_name)
                zones[zone_name] = zone

        communities = {}
        for i in range(rows_count):
            community_name = data["COMUNIDAD"][i]
            if community_name not in communities:
                zone = zones[data["ZONA"][i]]
                community = Community.objects.create(name=community_name, zone=zone)
                communities[community_name] = community                

        sectors = {}
        for i in range(rows_count):
            sector_name = data["SECTOR/IRRIGACION"][i]
            if sector_name not in sectors:
                community = communities[data["COMUNIDAD"][i]]
                sector = Sector.objects.create(name=sector_name, community=community)
                sectors[sector_name] = sector

        for i in range(rows_count):
            try:
                data_nombre = data["NOMBRE RESPONSABLE UP"][i]
                data_dni = data["DNI"][i]
                if not str(data_dni).isnumeric():
                    data_dni = 0
                Person.objects.get_or_create(name=data_nombre, dni=data_dni)
            except Exception as e:
                import pdb; pdb.set_trace()
                print('fila ' + str(i) + str(e))
