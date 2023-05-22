from django.contrib import admin
from core.models import (
    Activity,
    Person,
    VisitAnimal,
    VisitAnimalDetails,
    VisitGrass,
    Community,
    Diagnostic,
    Drug,
    SicknessObservation,
    Zone,
)


class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "dni", "sex")
    ordering = ["name"]


admin.site.register(Person, PersonAdmin)


admin.site.register(Activity)
admin.site.register(Community)
admin.site.register(Diagnostic)
admin.site.register(Drug)
admin.site.register(SicknessObservation)
admin.site.register(Zone)


class VisitDetailInline(admin.TabularInline):
    model = VisitAnimalDetails


class VisitAdmin(admin.ModelAdmin):
    inlines = [
        VisitDetailInline,
    ]


admin.site.register(VisitAnimal, VisitAdmin)
admin.site.register(VisitGrass)
