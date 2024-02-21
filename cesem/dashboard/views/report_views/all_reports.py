import datetime
import calendar
from dateutil.relativedelta import relativedelta
from core.models import (
    Activity,
    VisitAnimalHealth,
    Zone,
    VisitGrass,
    Community,
    VisitGeneticImprovementVacuno,
    VisitGeneticImprovementOvino,
    VisitGeneticImprovementAlpaca,
    VisitComponents,
    AnualPeriod
)
from django.db.models import F, Sum, Case, When, Value, Q, Count, CharField
from django.db.models.functions import ExtractWeek, Round, ExtractYear, Concat
from django.shortcuts import render
from itertools import chain

grass_quantity_var_sum = Round(
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

animal_health_quantity_var_sum = Sum(
    F("vacunos") + F("ovinos") + F("alpacas") + F("llamas") + F("canes")
)

vacuno_quantity_var_sum = Sum(
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

ovino_quantity_var_sum = Sum(
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

alpaca_quantity_var_sum = Sum(
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


def get_weekly_data(from_datepicker, to_datepicker, inform_type):
    animal_health_quantity_var = Count("id")
    grass_quantity_var = Count("id")
    vacuno_quantity_var = Count("id")
    ovino_quantity_var = Count("id")
    alpaca_quantity_var = Count("id")

    if inform_type == "sum":
        animal_health_quantity_var = animal_health_quantity_var_sum
        grass_quantity_var = grass_quantity_var_sum
        vacuno_quantity_var = vacuno_quantity_var_sum
        ovino_quantity_var = ovino_quantity_var_sum
        alpaca_quantity_var = alpaca_quantity_var_sum

    animals_data = (
        VisitAnimalHealth.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values("activity__id", "visited_at")
        .annotate(quantity=animal_health_quantity_var)
        .order_by("visited_at")
    )

    grass_data = (
        VisitGrass.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values("activity__id", "visited_at")
        .annotate(quantity=grass_quantity_var)
        .order_by("visited_at")
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values("activity__id", "visited_at")
        .annotate(quantity=vacuno_quantity_var)
        .order_by("visited_at")
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values("activity__id", "visited_at")
        .annotate(quantity=ovino_quantity_var)
        .order_by("visited_at")
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values("activity__id", "visited_at")
        .annotate(quantity=alpaca_quantity_var)
        .order_by("visited_at")
    )

    if inform_type == "sum":
        # cantidad de asistentes
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
            )
            .values("id", "activity__id", "visited_at")
            .annotate(quantity=Count("id"))
            .order_by("visited_at")
        )

    else:
        # cantidad de capacitaciones que se dieron
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
            )
            .annotate(location_concat=Concat(F('production_unit__zone'), F('production_unit__community'), F('production_unit__sector'), output_field=CharField()))
            .values(
                "visited_at",
                "activity__id",
            )
            .annotate(quantity=Count('location_concat', distinct=True))
            .order_by("visited_at")
        )

    data = list(
        chain(
            animals_data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
            components_data,
        )
    )

    return data


def get_weeks_number(from_week_year, to_week_year):
    weeks_number = {}
    week_from, year_from = from_week_year
    week_to, year_to = to_week_year

    for year in range(year_from, year_to + 1):
        week_from_iter = week_from if year == year_from else 1
        week_to_iter = week_to if year == year_to else get_last_week_of_year(year)
        for week in range(week_from_iter, week_to_iter + 1):
            weeks_number[(week, year)]= ""

    # todas las semanas existentes dentro del from y el to
    return weeks_number


def get_last_week_of_year(year):
    last_day = datetime.datetime(year, 12, 31)
    return last_day.isocalendar()[1]


def get_week_year_of(date_str):
    if isinstance(date_str, str):
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return (date.isocalendar()[1], date.isocalendar()[0])


def get_activities_data(data, activities):
    """
    Format:
    {
        'activity_key':{ 
            ('week', 'year'): value
        },
        'activity_key':{ 
			('week', 'year'): value
		}
    }
    """
    activities_data = {}
    for d in data:
        activity_id = d.get('activity__id')
        visited_at = d.get('visited_at')
        quantity = d.get('quantity')
        year, week, _ = visited_at.isocalendar()

        if activity_id in activities_data:
            if (week, year) in activities_data[activity_id]:
                activities_data[activity_id][(week, year)] += quantity
            else:
                activities_data[activity_id][(week, year)] = quantity
        else:
            activities_data[activity_id] = {}
            activities_data[activity_id][(week, year)] = quantity

    sub_activity_data = get_data_of_sub_activity(activities, activities_data)
    activities_data.update(sub_activity_data)

    return activities_data


def get_anual_period():
    from_anual_period_object = AnualPeriod.objects.first()
    from_anual_period = from_anual_period_object.date_from

    if from_anual_period.month == 2 and from_anual_period.day == 29:
        to_anual_period = datetime.date(from_anual_period.year+1, 2, 28)
    else:
        to_anual_period = from_anual_period.replace(year=from_anual_period.year+1) - datetime.timedelta(days=1)
    
    return from_anual_period, to_anual_period


def get_last_years(from_anual_period):
    period_year = from_anual_period.year

    return [str(period_year - 2), str(period_year - 1), str(period_year)]


def get_current_period(year, from_anual_period, to_anual_period):
    month_from_period = from_anual_period.month
    day_from_period = from_anual_period.day
    month_to_period = to_anual_period.month
    day_to_period = to_anual_period.day

    # para el caso de que alguna de las fechas haya sido 29 pero no exista en el año actual
    if day_from_period == 29 and month_from_period == 2 and not calendar.isleap(year):
        default_from = datetime.date(year, 2, 28)
    else:
        default_from = datetime.date(year, month_from_period, day_from_period)
    
    if month_from_period == 1 and day_from_period == 1:
        default_to_year = year
    else:
        default_to_year = year + 1
    
    # para el caso de que alguna de las fechas haya sido 29 pero no exista en el año actual
    if day_to_period == 29 and month_to_period == 2 and not calendar.isleap(default_to_year):
        default_to = datetime.date(default_to_year, 2, 28)
    else:
        default_to = datetime.date(default_to_year, month_to_period, day_to_period)
    
    return default_from.strftime('%Y-%m-%d'), default_to.strftime('%Y-%m-%d')


def generate_period_list(from_date, to_date):
    # Convertir las fechas de entrada a objetos datetime.date
    from_date_obj = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date_obj = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

    periods = []

    current_from = from_date_obj
    current_to = (from_date_obj  + relativedelta(months=1)) - datetime.timedelta(days=1)
    for i in range(12):
        periods.append({
            "month": i+1,
            "from_p": current_from.strftime('%Y-%m-%d'),
            "to_p": current_to.strftime('%Y-%m-%d')
        })
        current_from = current_to + datetime.timedelta(days=1)
        current_to = (current_from  + relativedelta(months=1)) - datetime.timedelta(days=1)

    return periods


def get_monthly_data(default_from, default_to, periods, inform_type):
    whens = []
    for period in periods:
        whens.append(
            When(
                Q(visited_at__gte=period.get("from_p"))
                & Q(visited_at__lte=period.get("to_p")),
                then=Value(period.get("month")),
            )
        )
    # whens.append(default="default")

    animal_health_quantity_var = Count("id")
    grass_quantity_var = Count("id")
    vacuno_quantity_var = Count("id")
    ovino_quantity_var = Count("id")
    alpaca_quantity_var = Count("id")
    if inform_type == "sum":
        animal_health_quantity_var = animal_health_quantity_var_sum
        grass_quantity_var = grass_quantity_var_sum
        vacuno_quantity_var = vacuno_quantity_var_sum
        ovino_quantity_var = ovino_quantity_var_sum
        alpaca_quantity_var = alpaca_quantity_var_sum

    animals_data = (
        VisitAnimalHealth.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .annotate(month=Case(*whens))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=animal_health_quantity_var)
        .order_by("activity__id", "month")
    )

    grass_data = (
        VisitGrass.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .annotate(month=Case(*whens))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=grass_quantity_var)
        .order_by("activity__id", "month")
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .annotate(month=Case(*whens))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=vacuno_quantity_var)
        .order_by("activity__id", "month")
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .annotate(month=Case(*whens))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=ovino_quantity_var)
        .order_by("activity__id", "month")
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .annotate(month=Case(*whens))
        .values(
            "activity__id",
            "month",
        )
        .annotate(quantity=alpaca_quantity_var)
        .order_by("activity__id", "month")
    )

    if inform_type == "sum":
        # cantidad de asistentes
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=default_from, visited_at__lte=default_to
            )
            .annotate(month=Case(*whens))
            .values("activity__id", "month")
            .annotate(quantity=Count("id"))
            .order_by("activity__id", "month")
        )

    else:
        # cantidad de capacitaciones que se dieron
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=default_from, visited_at__lte=default_to
            )
            .annotate(month=Case(*whens))
            .values(
                "month",
                "production_unit__zone",
                "production_unit__community",
                "production_unit__sector",
                "activity__id",
            )
            .annotate(quantity=Count("visited_at", distinct=True))
            .order_by("activity__id", "month")
        )

    data = list(
        chain(
            animals_data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
            components_data,
        )
    )
    return data


def get_monthly_activities_data(data, activities):
    activities_data = {}

    for s in data:
        activity_key = s.get("activity__id")
        month_key = s.get("month")
        value = s.get("quantity")

        if activity_key not in activities_data:
            activities_data[activity_key] = {}
        if activities_data[activity_key].get(month_key): #este caso se ha agregado porque en componentes se vio el caso que habian 2 valores para la misma celda, por tanto se sumarán
            activities_data[activity_key][month_key] += value
        else:
            activities_data[activity_key][month_key] = value

    sub_activity_data = get_data_of_sub_activity(activities, activities_data)
    activities_data.update(sub_activity_data)

    return activities_data


def get_yearly_data(default_from, default_to, inform_type):
    animal_health_quantity_var = Count("id")
    grass_quantity_var = Count("id")
    vacuno_quantity_var = Count("id")
    ovino_quantity_var = Count("id")
    alpaca_quantity_var = Count("id")

    if inform_type == "sum":
        animal_health_quantity_var = animal_health_quantity_var_sum
        grass_quantity_var = grass_quantity_var_sum
        vacuno_quantity_var = vacuno_quantity_var_sum
        ovino_quantity_var = ovino_quantity_var_sum
        alpaca_quantity_var = alpaca_quantity_var_sum

    animals_data = (
        VisitAnimalHealth.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .values(
            "activity__id",
        )
        .annotate(quantity=animal_health_quantity_var)
        .order_by(
            "activity__id",
        )
    )

    grass_data = (
        VisitGrass.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .values(
            "activity__id",
        )
        .annotate(quantity=grass_quantity_var)
        .order_by(
            "activity__id",
        )
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .values(
            "activity__id",
        )
        .annotate(quantity=vacuno_quantity_var)
        .order_by(
            "activity__id",
        )
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .values(
            "activity__id",
        )
        .annotate(quantity=ovino_quantity_var)
        .order_by(
            "activity__id",
        )
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.filter(
            visited_at__gte=default_from, visited_at__lte=default_to
        )
        .values(
            "activity__id",
        )
        .annotate(quantity=alpaca_quantity_var)
        .order_by(
            "activity__id",
        )
    )

    if inform_type == "sum":
        # cantidad de asistentes
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=default_from, visited_at__lte=default_to
            )
            .values("activity__id")
            .annotate(quantity=Count("id"))
            .order_by("activity__id")
        )

    else:
        # cantidad de capacitaciones que se dieron
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=default_from, visited_at__lte=default_to
            )
            .values(
                "production_unit__zone",
                "production_unit__community",
                "production_unit__sector",
                "activity__id",
            )
            .annotate(quantity=Count("visited_at", distinct=True))
            .order_by("activity__id")
        )

    data = list(
        chain(
            animals_data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
            components_data,
        )
    )
    return data


def get_yearly_activities_data(data, activities):
    activities_data = {}
    for s in data:
        activity_key = s.get("activity__id")
        value = s.get("quantity")
        if activities_data.get(activity_key): #este caso se ha agregado porque en componentes se vio el caso que habian 2 valores para la misma celda, por tanto se sumarán
            activities_data[activity_key] += value    
        else:
            activities_data[activity_key] = value

    sub_activity_data = {}
    for a in activities:
        if is_sub_activity(a):
            sub_activity = a
            for activity_key in activities_data:
                if activity_is_in_sub_activity(activities, activity_key, sub_activity):
                    if sub_activity.id not in sub_activity_data:
                        sub_activity_data[sub_activity.id] = 0
                    at = activities.get(id=activity_key)
                    if at.sum_in_parent:
                        sub_activity_data[sub_activity.id] += activities_data[activity_key]
    
    activities_data.update(sub_activity_data)
    
    return activities_data


def report_weekly(request):
    currentdate = datetime.date.today()
    default_from = "{}-01-01".format(currentdate.year)
    default_to = currentdate.strftime("%Y-%m-%d")
    from_datepicker = request.GET.get("from_datepicker", default_from)
    to_datepicker = request.GET.get("to_datepicker", default_to)

    # TODO: create a function to replace year_prev, inform_type_prev
    inform_type_prev = request.GET.get("type_prev", "count")
    inform_type = request.GET.get("type", inform_type_prev)

    activities = Activity.objects.all().order_by("position")

    data = get_weekly_data(from_datepicker, to_datepicker, inform_type)
    activities_data = get_activities_data(data, activities)
    weeks_number = get_weeks_number(get_week_year_of(from_datepicker), get_week_year_of(to_datepicker))

    return render(request, "dashboard/report_weekly.html", locals())


def report_monthly(request):
    from_anual_period, to_anual_period = get_anual_period()
    filter_years_list = get_last_years(from_anual_period)

    year_prev = int(request.GET.get("year_prev", from_anual_period.year))
    year = int(request.GET.get("year", year_prev))
    year_str = str(year)
    default_from, default_to = get_current_period(year, from_anual_period, to_anual_period)

    inform_type_prev = request.GET.get("type_prev", "count")
    inform_type = request.GET.get("type", inform_type_prev)

    activities = Activity.objects.all().order_by("position")
    periods = generate_period_list(default_from, default_to)

    data = get_monthly_data(default_from, default_to, periods, inform_type)
    activities_data = get_monthly_activities_data(data, activities)

    return render(request, "dashboard/report_monthly.html", locals())


def report_yearly(request):
    from_anual_period, to_anual_period = get_anual_period()
    filter_years_list = get_last_years(from_anual_period)

    year_prev = int(request.GET.get("year_prev", from_anual_period.year))
    year = int(request.GET.get("year", year_prev))
    year_str = str(year)

    default_from, default_to = get_current_period(year, from_anual_period, to_anual_period)

    inform_type_prev = request.GET.get("type_prev", "count")
    inform_type = request.GET.get("type", inform_type_prev)
    activities = Activity.objects.all().order_by("position")

    data = get_yearly_data(default_from, default_to, inform_type)
    activities_data = get_yearly_activities_data(data, activities)

    return render(request, "dashboard/report_yearly.html", locals())


def report_zones(request):
    currentdate = datetime.date.today()
    default_from = "{}-01-01".format(currentdate.year)
    default_to = currentdate.strftime("%Y-%m-%d")
    from_datepicker = request.GET.get("from_datepicker", default_from)
    to_datepicker = request.GET.get("to_datepicker", default_to)

    inform_type_prev = request.GET.get("type_prev", "count")
    inform_type = request.GET.get("type", inform_type_prev)

    activities = Activity.objects.all().order_by("position")
    zones = Zone.objects.all().order_by("name")

    animal_health_quantity_var = Count("id")
    grass_quantity_var = Count("id")
    vacuno_quantity_var = Count("id")
    ovino_quantity_var = Count("id")
    alpaca_quantity_var = Count("id")
    if inform_type == "sum":
        animal_health_quantity_var = animal_health_quantity_var_sum
        grass_quantity_var = grass_quantity_var_sum
        vacuno_quantity_var = vacuno_quantity_var_sum
        ovino_quantity_var = ovino_quantity_var_sum
        alpaca_quantity_var = alpaca_quantity_var_sum

    animals_data = (
        VisitAnimalHealth.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=animal_health_quantity_var)
        .order_by("production_unit__zone")
    )

    grass_data = (
        VisitGrass.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=grass_quantity_var)
        .order_by("production_unit__zone")
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=vacuno_quantity_var)
        .order_by("production_unit__zone")
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=ovino_quantity_var)
        .order_by("production_unit__zone")
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__zone",
        )
        .annotate(quantity=alpaca_quantity_var)
        .order_by("production_unit__zone")
    )

    if inform_type == "sum":
        # cantidad de asistentes
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
            )
            .values("activity__id", "production_unit__zone")
            .annotate(quantity=Count("id"))
            .order_by("production_unit__zone")
        )

    else:
        # cantidad de capacitaciones que se dieron
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
            )
            .values(
                "production_unit__zone",
                "activity",
            )
            .annotate(quantity=Count("visited_at", distinct=True))
            .order_by("production_unit__zone")
        )

    data = list(
        chain(
            animals_data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
            components_data,
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
    currentdate = datetime.date.today()
    default_from = "{}-01-01".format(currentdate.year)
    default_to = currentdate.strftime("%Y-%m-%d")
    from_datepicker = request.GET.get("from_datepicker", default_from)
    to_datepicker = request.GET.get("to_datepicker", default_to)

    inform_type_prev = request.GET.get("type_prev", "count")
    inform_type = request.GET.get("type", inform_type_prev)

    activities = Activity.objects.all().order_by("position")
    communities = Community.objects.all().order_by("name")

    animal_health_quantity_var = Count("id")
    grass_quantity_var = Count("id")
    vacuno_quantity_var = Count("id")
    ovino_quantity_var = Count("id")
    alpaca_quantity_var = Count("id")
    if inform_type == "sum":
        animal_health_quantity_var = animal_health_quantity_var_sum
        grass_quantity_var = grass_quantity_var_sum
        vacuno_quantity_var = vacuno_quantity_var_sum
        ovino_quantity_var = ovino_quantity_var_sum
        alpaca_quantity_var = alpaca_quantity_var_sum

    animals_data = (
        VisitAnimalHealth.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=animal_health_quantity_var)
        .order_by("production_unit__community")
    )

    grass_data = (
        VisitGrass.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=grass_quantity_var)
        .order_by("production_unit__community")
    )

    genetic_improvement_vacuno_data = (
        VisitGeneticImprovementVacuno.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=vacuno_quantity_var)
        .order_by("production_unit__community")
    )

    genetic_improvement_ovino_data = (
        VisitGeneticImprovementOvino.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=ovino_quantity_var)
        .order_by("production_unit__community")
    )

    genetic_improvement_alpaca_data = (
        VisitGeneticImprovementAlpaca.objects.filter(
            visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
        )
        .values(
            "activity",
            "production_unit__community",
        )
        .annotate(quantity=alpaca_quantity_var)
        .order_by("production_unit__community")
    )

    if inform_type == "sum":
        # cantidad de asistentes
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
            )
            .values("activity__id", "production_unit__community")
            .annotate(quantity=Count("id"))
            .order_by("production_unit__community")
        )

    else:
        # cantidad de capacitaciones que se dieron
        components_data = (
            VisitComponents.objects.filter(
                visited_at__gte=from_datepicker, visited_at__lte=to_datepicker
            )
            .values(
                "production_unit__community",
                "activity",
            )
            .annotate(quantity=Count("visited_at", distinct=True))
            .order_by("production_unit__community")
        )

    data = list(
        chain(
            animals_data,
            grass_data,
            genetic_improvement_vacuno_data,
            genetic_improvement_ovino_data,
            genetic_improvement_alpaca_data,
            components_data,
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
    # for components II and III logic
    if (
        activity.position.startswith("2.") or activity.position.startswith("3.")
    ) and len(activity.position) == 3:
        return True

    letters = list(activity.position)
    points = filter(lambda letter: letter == ".", letters)
    points = list(points)
    points = len(points)

    return (
        points == 2
    )  # this is the numbers of points considered to sum the subactivities


def activity_is_in_sub_activity(activities, activity_key, sub_activity):
    for a in activities:
        if a.id == activity_key:
            return a.parent == sub_activity
    return False


def get_data_of_sub_activity(activities, activities_data):
    sub_activity_data = {}
    for a in activities:
        if is_sub_activity(a):
            sub_activity = a
            for activity_key in activities_data:
                if activity_is_in_sub_activity(activities, activity_key, sub_activity):
                    if sub_activity.id not in sub_activity_data:
                        sub_activity_data[sub_activity.id] = {}
                    at = activities.get(id=activity_key)
                    if at.sum_in_parent:
                        for related_key in activities_data[activity_key]:
                            if related_key not in sub_activity_data[sub_activity.id]:
                                sub_activity_data[sub_activity.id][related_key] = 0
                            sub_activity_data[sub_activity.id][
                                related_key
                            ] += activities_data[activity_key][related_key]

    return sub_activity_data
