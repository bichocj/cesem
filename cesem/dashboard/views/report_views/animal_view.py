from core.models import Activity, VisitAnimal
from django.db.models import F, Sum
from django.db.models.functions import ExtractWeek, ExtractYear
from django.shortcuts import render


def report(request):
    year = 2022
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
                F("cattle") + F("sheep") + F("alpacas") + F("llamas") + F("canes")
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

    return render(request, "dashboard/home.html", locals())
