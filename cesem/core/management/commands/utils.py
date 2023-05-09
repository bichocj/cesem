from django.core.management.base import BaseCommand
from core.models import Person, Zone, Activity, Community, Sector, ProductionUnit

class HelperCommand(BaseCommand):
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
            '--creates_if_none',
            default=False,
            help='it creates activites, diagnostics and sickness if doesnt exists',
        )

    def get_person(self, name, dni=None, sex=None):
        sex_data = None
        if sex == 'M':
            sex_data = Person.Sexs.MALE
        if sex == 'F':
            sex_data = Person.Sexs.FEMALE

        person = None
        if name in self.people_names:
            person = self.people_names[name]
        else:
            try:
                person = Person.objects.get(name=name)
            except Person.DoesNotExist:
                person = Person.objects.create(name=name, dni= dni, sex=sex_data)
                self.people_names[name] = person
        return person
    
    def get_zone(self, name, creates_if_none):
        zone = None
        if name in self.zones_names:
            zone = self.zones_names[name]
        else:
            if creates_if_none:
                zone = Zone.objects.create(name=name)
                self.zones_names[name] = zone
            else:
                raise Zone.DoesNotExist()
        return zone

    def get_community(self, name, zone, creates_if_none):        
        community = None
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
        if name in self.activities_names:
            activity = self.activities_names[name]
        else:
            if creates_if_none:
                activity = Activity.objects.create(name=name, short_name=name)
                self.activities_names[name] = activity
            else:
                raise Activity.DoesNotExist()
        return activity

    
    def get_production_unit(self, 
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
                            creates_if_none=False
                            ):
        zone = self.get_zone(data_zone, creates_if_none)
        community = self.get_community(data_community, zone, creates_if_none)
        sector = self.get_sector(data_sector, community, creates_if_none)
        up_responsable = self.get_person(data_up_responsable_name, data_up_responsable_dni, data_up_responsable_sex)
        up_member = self.get_person(data_up_member_name, data_up_member_dni, data_up_member_sex)

        production_unit, created = ProductionUnit.objects.get_or_create(
            zone=zone, 
            community=community, 
            sector=sector, 
            person_responsable=up_responsable, 
            person_member=up_member,            
        )

        if created:
            if production_unit.tipology != data_tipology or production_unit.is_pilot != data_is_pilot:
                production_unit.tipology = data_tipology
                production_unit.is_pilot = data_is_pilot
                production_unit.save()

        return production_unit