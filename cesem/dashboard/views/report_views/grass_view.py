from core.models import Activity, VisitGrass, Zone
from django.db.models import F, Sum
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractYear, Lower
from django.shortcuts import render

year = 2022

mapping_activity_quantity = {
    "instalación de parcelas de avena forrajera asociado con vicia": "avena_vicia_planted_hectares",
    "instalación de parcelas de avena forrajera": "avena_planted_hectares",
    "entrega de semilla de avena tayco": "oat_kg",
    "entrega de semillas de vicia": "vicia_kg",
    "entrega de fertilizante nitrogenado": "fertilizer",
    "preparación de terreno para siembra del cultivo anual": "plow_hours",  # sum "dredge_hours" after
    "instalación de alfalfa + dactylis": "alfalfa_dactylis_planted_hectares",
    "instalación de rye grass + trébol blanco": "ryegrass_trebol_planted_hectares",
    "entrega de semilla de alfalfa (25 Kg/Ha)": "alfalfa_kg",
    "entrega de semilla de dactylis (5 Kg/Ha)": "dactylis_kg",
    "entrega de semilla de ryegrass (20 Kg/Ha)": "ryegrass_kg",
    "entrega de semilla de trébol blanco (5 Kg/Ha)": "trebol_b_kg",
    # "adquisición de fertilizante fosforado (02 bolsas/ha) Zona 9": "fertilizer",
    "preparación de terreno para siembra del cultivo de pastos perennes": "plow_hours",  # sum "dredge_hours" after
    "curso taller en instalación de pastos anuales y perennes (parcelas demostrativas)": "technical_training_perennial",  # sum "technical_training_anual" after
    "curso taller en manejo y conservación de forrajes cultivados": "technical_training_conservation",
    "asistencia técnica": "technical_assistance",
    "evaluación de intensión de siembra de cultivos anuales y perennes": "planting_intention_hectares",
    "evaluación de cosecha de pastos cultivados anuales (monitoreo)": "anual_yield",
    "evaluación de cosecha de pastos cultivados perennes (monitoreo)": "perennial_yield",
}


def report_weekly(request):
    activities = Activity.objects.all().order_by("position")

    data = (
        VisitGrass.objects.filter(visited_at__year=year)
        .annotate(week=ExtractWeek("visited_at"))
        .values(
            "activity__id",
            "week",
        )
        .annotate(quantity=mapping_activity_quantity.get(Lower("activity__name")))
        .order_by("week")
    )

    activities_data = {}
    weeks_number = {}

    for s in data:
        activity_key = s.get("activity__id")
        week_key = s.get("week")
        value = s.get("quantity")

        if activity_key not in activities_data:
            activities_data[activity_key] = {}
        activities_data[activity_key][week_key] = value

        weeks_number[week_key] = ""

    sub_activity_data = {}
    for a in activities:
        if is_sub_activity(a):
            sub_activity = a
            for activity_key in activities_data:
                if activity_is_in_sub_activity(activities, activity_key, sub_activity):
                    if sub_activity.id not in sub_activity_data:
                        sub_activity_data[sub_activity.id] = {}
                    for week_key in activities_data[activity_key]:
                        if week_key not in sub_activity_data[sub_activity.id]:
                            sub_activity_data[sub_activity.id][week_key] = 0
                        sub_activity_data[sub_activity.id][week_key] += activities_data[
                            activity_key
                        ][week_key]

    activities_data.update(sub_activity_data)

    return render(request, "dashboard/report_weekly.html", locals())


"""
def report_monthly(request):
    activities = Activity.objects.all().order_by("position")

    data = (
        VisitAnimalHealth.objects.filter(visited_at__year=year)
        .annotate(month=ExtractMonth("visited_at"))
        .values(
            "activity__id",
            "month",
        )
        .annotate(
            sum_animals=Sum(
                F("vacunos") + F("ovinos") + F("alpacas") + F("llamas") + F("canes")
            )
        )
        .order_by("activity__id", "month")
    )

    print(data.query)

    activities_data = {}
    month_number = {}

    for s in data:
        activity_key = s.get("activity__id")
        month_key = s.get("month")
        value = s.get("sum_animals")

        if activity_key not in activities_data:
            activities_data[activity_key] = {}
        activities_data[activity_key][month_key] = value

        month_number[month_key] = ""

    sub_activity_data = {}
    for a in activities:
        if is_sub_activity(a):
            sub_activity = a
            for activity_key in activities_data:
                if activity_is_in_sub_activity(activities, activity_key, sub_activity):
                    if sub_activity.id not in sub_activity_data:
                        sub_activity_data[sub_activity.id] = {}
                    for month_key in activities_data[activity_key]:
                        if month_key not in sub_activity_data[sub_activity.id]:
                            sub_activity_data[sub_activity.id][month_key] = 0
                        sub_activity_data[sub_activity.id][
                            month_key
                        ] += activities_data[activity_key][month_key]

    activities_data.update(sub_activity_data)

    return render(request, "dashboard/report_monthly.html", locals())


def report_zones(request):
    activities = Activity.objects.all().order_by("position")
    zones = Zone.objects.all().order_by("name")
    data = (
        VisitAnimalHealth.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(
            sum_animals=Sum(
                F("vacunos") + F("ovinos") + F("alpacas") + F("llamas") + F("canes")
            )
        )
        .filter(visited_at__year=year)
        .order_by("production_unit__zone")
    )

    activities_data = {}

    for s in data:
        activity_key = s.get("activity")
        week_key = s.get("production_unit__zone")
        value = s.get("sum_animals")

        if activity_key not in activities_data:
            activities_data[activity_key] = {}
        activities_data[activity_key][week_key] = value

    return render(request, "dashboard/report_zones.html", locals())
"""


def is_sub_activity(activity):
    letters = list(activity.position)
    points = filter(lambda letter: letter == ".", letters)
    points = list(points)
    points = len(points)
    return points == 1


def activity_is_in_sub_activity(activities, activity_key, sub_activity):
    for a in activities:
        if a.id == activity_key:
            return a.parent == sub_activity
    return False
