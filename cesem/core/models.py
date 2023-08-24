from django.db import models


class Person(models.Model):
    class Sexs(models.IntegerChoices):
        FEMALE = 0, ("femenino")
        MALE = 1, ("masculino")

    class Titles(models.IntegerChoices):
        tec = 0, ("tec.")
        mvz = 1, ("mvz.")

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "personas"
        ordering = ("name",)

    dni = models.IntegerField("dni", null=True, blank=True)
    name = models.CharField("nombres", max_length=50)
    last_name = models.CharField("apellidos", max_length=50, blank=True, null=True)
    sex = models.IntegerField("sexo", choices=Sexs.choices, blank=True, null=True)
    title = models.IntegerField("titulo", choices=Titles.choices, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Zone(models.Model):
    name = models.CharField("nombre", max_length=20, unique=True)

    class Meta:
        verbose_name = "zona"
        verbose_name_plural = "zonas"

    def __str__(self) -> str:
        return self.name


class Community(models.Model):
    name = models.CharField("nombre", max_length=20, unique=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="zona")

    class Meta:
        verbose_name = "comunidad"
        verbose_name_plural = "comunidades"

    def __str__(self) -> str:
        return self.name


class Sector(models.Model):
    name = models.CharField("nombre", max_length=20, unique=True)
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, verbose_name="comunidad"
    )

    class Meta:
        verbose_name = "sector"
        verbose_name_plural = "sectores"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Activity(models.Model):
    class Meta:
        verbose_name = "actividad"
        verbose_name_plural = "actividades"
        ordering = ("position",)

    position = models.CharField("posición", max_length=6)
    name = models.CharField("nombre", max_length=100)
    short_name = models.CharField("nombre corto", default="", max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        verbose_name="actividad superior",
    )
    um = models.CharField("unidad de medida", null=True, blank=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class SicknessObservation(models.Model):
    name = models.CharField("nombre", max_length=50)

    class Meta:
        verbose_name = "enfermedad/observación"
        verbose_name_plural = "enfermedades/observaciones"

    def __str__(self) -> str:
        return self.name


class Diagnostic(models.Model):
    name = models.CharField(
        "observación", max_length=50
    )  # the name 'name' allow us an easy sync in sync_masters func

    class Meta:
        verbose_name = "diagnostico"
        verbose_name_plural = "diagnosticos"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Drug(models.Model):
    class UnitMeasurement(models.IntegerChoices):
        ml = 0, ("ml.")
        gr = 1, ("gr.")

    name = models.CharField("nombre", max_length=50)
    um = models.CharField("unidad de medida", max_length=100)
    # , choices=UnitMeasurement.choices, default=0

    class Meta:
        verbose_name = "farmaco"
        verbose_name_plural = "farmacos"

    def __str__(self) -> str:
        return self.name


class ProductionUnit(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="zona")
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, verbose_name="comunidad"
    )
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name="sector")
    person_responsable = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_responsable_animal",
        verbose_name="up. responsable",
    )
    person_member = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_member_animal",
        verbose_name="up. integrante",
    )
    tipology = models.IntegerField(default=0)
    is_pilot = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Unidad de Producción"
        verbose_name_plural = "Unidades de Producción"
        ordering = ("zone", "person_responsable")


class VisitAnimal(models.Model):
    visited_at = models.DateField(
        "fecha de creación", blank=True, null=True
    )  # Because current XLS doesn't have all dates
    production_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE, verbose_name="UP"
    )
    employ_specialist = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_specialist_animal",
        verbose_name="personal especialista",
    )
    employ_responsable = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_responsable_animal",
        verbose_name="personal responsable",
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name="actividad"
    )
    sickness_observation = models.ForeignKey(
        SicknessObservation,
        on_delete=models.CASCADE,
        verbose_name="enfermedad/observación",
    )
    diagnostic = models.ForeignKey(
        Diagnostic, on_delete=models.CASCADE, verbose_name="diagnostico"
    )
    vaca = models.IntegerField("vaca", default=0)
    vaquillona = models.IntegerField("vaquillona", default=0)
    vaquilla = models.IntegerField("vaquilla", default=0)
    terreno = models.IntegerField("terreno", default=0)
    torete = models.IntegerField("torete", default=0)
    toro = models.IntegerField("toro", default=0)
    vacunos = models.IntegerField("vacunos", default=0)
    ovinos = models.IntegerField("ovinos", default=0)
    alpacas = models.IntegerField("alpacas", default=0)
    llamas = models.IntegerField("llamas", default=0)
    canes = models.IntegerField("canes", default=0)

    class Meta:
        verbose_name = "visita animal"
        verbose_name_plural = "visitas animales"
        ordering = ("visited_at", "production_unit")


class VisitAnimalDetails(models.Model):
    visit = models.ForeignKey(VisitAnimal, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, verbose_name="farmacos")
    quantity = models.IntegerField("cantidad", default=0)

    class Meta:
        verbose_name = "visita animal - detalle"
        verbose_name_plural = "visitas animales - detalles"


class VisitGrass(models.Model):
    visited_at = models.DateField(
        "fecha de creacion", blank=True, null=True
    )  # Because current XLS doesn't have all dates
    production_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE, verbose_name="UP"
    )
    utm_coordenate = models.CharField(
        "coordenadas UTM anuales", max_length=30, null=True, blank=True
    )
    producer_classification = models.CharField(
        "tipificación de productores", max_length=30, null=True, blank=True
    )
    employ_specialist = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_specialist_grass",
        verbose_name="personal especialista",
    )
    employ_responsable = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_responsable_grass",
        verbose_name="personal responsable",
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name="actividad"
    )
    planting_intention_hectares = models.DecimalField(
        "has. intens. de siembra",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    ground_analysis = models.DecimalField(
        "anal. suelo", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    plow_hours = models.DecimalField(
        "horas arado", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    dredge_hours = models.DecimalField(
        "horas rastra",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    oat_kg = models.DecimalField(
        "kg avena", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    vicia_kg = models.DecimalField(
        "kg vicia", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    alfalfa_kg = models.DecimalField(
        "kg alfalfa", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    dactylis_kg = models.DecimalField(
        "kg dactylis", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    ryegrass_kg = models.DecimalField(
        "kg ryegrass", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    trebol_b_kg = models.DecimalField(
        "kg trebol", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    fertilizer = models.DecimalField(
        "fertilizante",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    avena_planted_hectares = models.DecimalField(
        "has. siembra avena",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    avena_vicia_planted_hectares = models.DecimalField(
        "has. siembra avena/vicia",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    alfalfa_dactylis_planted_hectares = models.DecimalField(
        "has. siembra alfalfa dactylis",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    ryegrass_trebol_planted_hectares = models.DecimalField(
        "has. siembra ryegrass trebol",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    anual_yield = models.DecimalField(
        "rendimiento anuales kg mv/ha",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    technical_assistance = models.DecimalField(
        "asistencia técnica",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    direct_grazing = models.DecimalField(
        "pastoreo directo (%)",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    hay = models.DecimalField(
        "heno (%)", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    ensilage = models.DecimalField(
        "ensilado (%)",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    bale = models.DecimalField(
        "pacas (%)", max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )
    perennial_grazing = models.DecimalField(
        "pastoreo % perenne",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    perennial_ensilage = models.DecimalField(
        "ensilado % perenne",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    perennial_yield = models.DecimalField(
        "rendimiento perenne",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    technical_training_perennial = models.DecimalField(
        "capacitación instalación perennes",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    technical_training_anual = models.DecimalField(
        "capacitación instalación anuales",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    technical_training_conservation = models.DecimalField(
        "capacitación manejo y conservación",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "visita pastos"
        verbose_name_plural = "visitas pastos"


class FilesChecksum(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    checksum = models.CharField(max_length=100)
    filename = models.TextField()
