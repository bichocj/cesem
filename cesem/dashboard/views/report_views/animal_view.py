from core.models import (
    Activity,
    VisitAnimalHealth,
    Zone,
    VisitGrass,
    Community,
    VisitGeneticImprovementVacuno,
    VisitGeneticImprovementOvino,
    VisitGeneticImprovementAlpaca,
)
from django.db.models import F, Sum, Case, When, Value, CharField
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractYear, Round
from django.shortcuts import render
from itertools import chain

year = 2022
"""
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
"""
grass_quantity_var = Round(
    Sum(
        F("planting_intention_hectares")
        + F("ground_analysis")
        + F("plow_hours")
        + F("dredge_hours")
        + F("oat_kg")
        + F("vicia_kg")
        + F("alfalfa_kg")
        + F("dactylis_kg")
        + F("ryegrass_kg")
        + F("trebol_b_kg")
        + F("fertilizer")
        + F("avena_planted_hectares")
        + F("avena_vicia_planted_hectares")
        + F("alfalfa_dactylis_planted_hectares")
        + F("ryegrass_trebol_planted_hectares")
        + F("anual_yield")
        + F("technical_assistance")
        + F("perennial_yield")
        + F("technical_training_perennial")
        + F("technical_training_anual")
        + F("technical_training_conservation")
    )
)

animal_health_quantity_var = Sum(
    F("vacunos") + F("ovinos") + F("alpacas") + F("llamas") + F("canes")
)

vacuno_quantity_var = Sum(
    F("pajillas_number")
    + F("male_attendance")
    + F("female_attendance")
    + F("technical_assistance_attendance")
    + F("pregnant")
    + F("empty")
    + F("male")
    + F("female")
    + F("death")
    + F("vacunos_number")
)

ovino_quantity_var = Sum(
    F("inseminated_sheeps_corriedale")
    + F("inseminated_sheeps_criollas")
    + F("course_male_attendance")
    + F("course_female_attendance")
    + F("selected_ovines")
    + F("technical_assistance_attendance")
    + F("pregnant")
    + F("empty")
    + F("not_evaluated")
    + F("synchronized_ovines")
    + F("baby_males")
    + F("baby_females")
    + F("baby_deaths")
    + F("ovinos_number")
)
alpaca_quantity_var = Sum(
    F("alpacas_empadradas_number")
    + F("training_male_attendance")
    + F("training_female_attendance")
    + F("technical_assistance_attendance")
    + F("hato_number")
    + F("selected_alpacas_number")
    + F("pregnant")
    + F("empty")
    + F("male_baby")
    + F("female_baby")
)


def report_weekly(request):
    activities = Activity.objects.all().order_by("position")

    data = (
        VisitAnimalHealth.objects.filter(visited_at__year=year)
        .annotate(week=ExtractWeek("visited_at"))
        .values(
            "id",
            "activity__id",
            "week",
        )
        .annotate(quantity=animal_health_quantity_var)
        .order_by("week")
    )

    grass_data = (
        VisitGrass.objects.filter(visited_at__year=year)
        .annotate(week=ExtractWeek("visited_at"))
        .values(
            "id",
            "activity__id",
            "week",
        )
        .annotate(quantity=grass_quantity_var)
        .order_by("week")
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.filter(visited_at__year=year)
        .annotate(week=ExtractWeek("visited_at"))
        .values(
            "id",
            "activity__id",
            "week",
        )
        .annotate(quantity=vacuno_quantity_var)
        .order_by("week")
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.filter(visited_at__year=year)
        .annotate(week=ExtractWeek("visited_at"))
        .values(
            "id",
            "activity__id",
            "week",
        )
        .annotate(quantity=ovino_quantity_var)
        .order_by("week")
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.filter(visited_at__year=year)
        .annotate(week=ExtractWeek("visited_at"))
        .values(
            "id",
            "activity__id",
            "week",
        )
        .annotate(quantity=alpaca_quantity_var)
        .order_by("week")
    )

    data = list(
        chain(
            data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
        )
    )

    activities_data = {}
    weeks_number = {}

    first_week = None
    for s in data:
        activity_key = s.get("activity__id")
        week_key = s.get("week")
        value = s.get("quantity")
        if not first_week:
            first_week = week_key

        if activity_key not in activities_data:
            activities_data[activity_key] = {}

        if week_key in activities_data[activity_key]:
            activities_data[activity_key][week_key] += value
        else:
            activities_data[activity_key][week_key] = value

        if week_key != first_week and weeks_number.get(week_key) != "":
            fill_previous_week(weeks_number, week_key)

        weeks_number[
            week_key
        ] = ""  # todas las semanas existentes en la data de animales + pastos, sin repetirse, mas las semanas faltantes

    sub_activity_data = get_data_of_sub_activity(activities, activities_data)
    activities_data.update(sub_activity_data)

    return render(request, "dashboard/report_weekly.html", locals())


def report_monthly(request):
    activities = Activity.objects.all().order_by("position")

    data = (
        VisitAnimalHealth.objects.filter(visited_at__year=year)
        .annotate(month=ExtractMonth("visited_at"))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=animal_health_quantity_var)
        .order_by("activity__id", "month")
    )

    grass_data = (
        VisitGrass.objects.filter(visited_at__year=year)
        .annotate(month=ExtractMonth("visited_at"))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=grass_quantity_var)
        .order_by("activity__id", "month")
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.filter(visited_at__year=year)
        .annotate(month=ExtractMonth("visited_at"))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=vacuno_quantity_var)
        .order_by("activity__id", "month")
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.filter(visited_at__year=year)
        .annotate(month=ExtractMonth("visited_at"))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=ovino_quantity_var)
        .order_by("activity__id", "month")
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.filter(visited_at__year=year)
        .annotate(month=ExtractMonth("visited_at"))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=alpaca_quantity_var)
        .order_by("activity__id", "month")
    )

    data = list(
        chain(
            data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
        )
    )

    activities_data = {}
    month_number = {}
    for s in data:
        activity_key = s.get("activity__id")
        month_key = s.get("month")
        value = s.get("quantity")

        if activity_key not in activities_data:
            activities_data[activity_key] = {}
        activities_data[activity_key][month_key] = value

        month_number[month_key] = ""

    sub_activity_data = get_data_of_sub_activity(activities, activities_data)
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
        .annotate(quantity=animal_health_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__zone")
    )

    grass_data = (
        VisitGrass.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=grass_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__zone")
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=vacuno_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__zone")
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=ovino_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__zone")
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=alpaca_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__zone")
    )

    data = list(
        chain(
            data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
        )
    )

    activities_data = {}
    for s in data:
        activity_key = s.get("activity")
        zone_key = s.get("production_unit__zone")
        value = s.get("quantity")

        if activity_key not in activities_data:
            activities_data[activity_key] = {}
        activities_data[activity_key][zone_key] = value

    sub_activity_data = get_data_of_sub_activity(activities, activities_data)
    activities_data.update(sub_activity_data)

    return render(request, "dashboard/report_zones.html", locals())


def report_community(request):
    activities = Activity.objects.all().order_by("position")
    communities = Community.objects.all().order_by("name")
    data = (
        VisitAnimalHealth.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=animal_health_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__community")
    )

    grass_data = (
        VisitGrass.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=grass_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__community")
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=vacuno_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__community")
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=ovino_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__community")
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.annotate(year=ExtractYear("visited_at"))
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=alpaca_quantity_var)
        .filter(visited_at__year=year)
        .order_by("production_unit__community")
    )

    data = list(
        chain(
            data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
        )
    )
    activities_data = {}

    for s in data:
        activity_key = s.get("activity")
        community_key = s.get("production_unit__community")
        value = s.get("quantity")

        if activity_key not in activities_data:
            activities_data[activity_key] = {}
        activities_data[activity_key][community_key] = value

    sub_activity_data = get_data_of_sub_activity(activities, activities_data)
    activities_data.update(sub_activity_data)

    return render(request, "dashboard/report_communities.html", locals())


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


def fill_previous_week(weeks_number, week_key):
    previous_week_key = week_key - 1
    if previous_week_key in weeks_number or week_key == 0:
        return 0
    weeks_number[previous_week_key] = ""
    return fill_previous_week(weeks_number, previous_week_key)


def get_data_of_sub_activity(activities, activities_data):
    sub_activity_data = {}
    for a in activities:
        if is_sub_activity(a):
            sub_activity = a
            for activity_key in activities_data:
                if activity_is_in_sub_activity(activities, activity_key, sub_activity):
                    if sub_activity.id not in sub_activity_data:
                        sub_activity_data[sub_activity.id] = {}
                    for related_key in activities_data[activity_key]:
                        if related_key not in sub_activity_data[sub_activity.id]:
                            sub_activity_data[sub_activity.id][related_key] = 0
                        sub_activity_data[sub_activity.id][
                            related_key
                        ] += activities_data[activity_key][related_key]

    return sub_activity_data
