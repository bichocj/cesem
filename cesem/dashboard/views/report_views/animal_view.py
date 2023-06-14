from core.models import Activity, VisitAnimal, Zone
from django.db.models import F, Sum
from django.db.models.functions import ExtractWeek, ExtractYear
from django.shortcuts import render

year = 2022


def report_weekly(request):
    activities = Activity.objects.all().order_by("position")

    data = (
        VisitAnimal.objects.annotate(year=ExtractYear("visited_at"))
        .annotate(week=ExtractWeek("visited_at"))
        .values(
            "activity",
            "week",
        )
        .annotate(
            sum_animals=Sum(
                F("vacunos") + F("ovinos") + F("alpacas") + F("llamas") + F("canes")
            )
        )
        .filter(visited_at__year=year)
        .order_by("week")
    )

    activities_data = {}
    weeks_number = {}

    for s in data:
        activity_key = s.get("activity")
        week_key = s.get("week")
        value = s.get("sum_animals")

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


def report_zones(request):
    activities = Activity.objects.all().order_by("position")
    zones = Zone.objects.all().order_by("name")
    data = (
        VisitAnimal.objects.annotate(year=ExtractYear("visited_at"))
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
