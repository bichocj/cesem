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
    Sector,
    FilesChecksum,
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


@admin.register(FilesChecksum)
class FilesChecksumAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)


class VisitDetailInline(admin.TabularInline):
    model = VisitAnimalDetails


@admin.register(VisitAnimal)
class VisitAdmin(admin.ModelAdmin):
    inlines = [
        VisitDetailInline,
    ]
