from django.contrib import admin
from core.models import (
    Activity,
    Person,
    VisitAnimalDeworming,
    VisitAnimalHealth,
    VisitAnimalHealthDetails,
    VisitGrass,
    Community,
    Diagnostic,
    Drug,
    SicknessObservation,
    Zone,
    Sector,
    FilesChecksum,
    VisitGeneticImprovementVacuno,
    VisitGeneticImprovementAlpaca,
    VisitGeneticImprovementOvino,
    VisitComponents,
    ProductionUnit,
    AnualPeriod,
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
admin.site.register(Sector)
admin.site.register(VisitGrass)
admin.site.register(ProductionUnit)


@admin.register(FilesChecksum)
class FilesChecksumAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_display = ("created_at", "filename")


class VisitDetailInline(admin.TabularInline):
    model = VisitAnimalHealthDetails


admin.site.register(VisitAnimalHealthDetails)


@admin.register(VisitAnimalHealth)
class VisitAdmin(admin.ModelAdmin):
    inlines = [
        VisitDetailInline,
    ]
    list_display = ("visited_at", "activity")
    list_filter = [
        "visited_at",
        "activity",
    ]


admin.site.register(VisitAnimalDeworming)
admin.site.register(VisitGeneticImprovementVacuno)
admin.site.register(VisitGeneticImprovementOvino)
admin.site.register(VisitGeneticImprovementAlpaca)
admin.site.register(VisitComponents)
admin.site.register(AnualPeriod)
