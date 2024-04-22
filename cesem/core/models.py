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
        unique_together = ("dni", "name")

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
    name = models.CharField("nombre", max_length=50)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="zona")
    zone_2 = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
        verbose_name="zona 2",
        related_name="zone_2",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "comunidad"
        verbose_name_plural = "comunidades"

    def __str__(self) -> str:
        return self.name


class Sector(models.Model):
    name = models.CharField("nombre", max_length=50, unique=True)
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, verbose_name="comunidad"
    )
    community_2 = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name="comunidad 2",
        related_name="comunidad_2",
        null=True,
        blank=True,
    )

    community_3 = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name="comunidad 3",
        related_name="comunidad_3",
        null=True,
        blank=True,
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

    position = models.CharField("posición", max_length=10)
    name = models.CharField("nombre", max_length=500)
    short_name = models.CharField("nombre corto", default="", max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        verbose_name="actividad superior",
    )
    sum_in_parent = models.BooleanField("sumar en resumen", default=True)
    um = models.CharField("unidad de medida", null=True, blank=True, max_length=50)
    meta_2022 = models.IntegerField("meta 2022", default=0)
    meta_2023 = models.IntegerField("meta 2023", default=0)
    meta_2024 = models.IntegerField("meta 2024", default=0)

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
    tipology = models.IntegerField("tipología de UP", default=0)
    is_pilot = models.BooleanField("UP es piloto?", default=False)
    is_official = models.BooleanField("es oficial?", default=True)

    class Meta:
        verbose_name = "Unidad de Producción"
        verbose_name_plural = "Unidades de Producción"
        ordering = ("person_responsable__name", "zone", )


class VisitGrass(models.Model):
    checksum = models.CharField(max_length=100, default="")
    visited_at = models.DateField(
        "fecha de visita", blank=True, null=True
    )  # Because current XLS doesn't have all dates
    production_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE, verbose_name="UP"
    )
    up_member = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_member_grass",
        verbose_name="up. integrante",
        null=True,
        blank=True,
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


class VisitAnimalHealth(models.Model):
    checksum = models.CharField(max_length=100, default="")
    visited_at = models.DateField(
        "fecha de visita", blank=True, null=True
    )  # Because current XLS doesn't have all dates
    production_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE, verbose_name="UP"
    )
    up_member = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_member_animal",
        verbose_name="up. integrante",
        null=True,
        blank=True,
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
        verbose_name = "visita sanidad animal"
        verbose_name_plural = "visitas sanidad animal"
        ordering = ("visited_at", "production_unit")
    


class VisitAnimalHealthDetails(models.Model):
    visit = models.ForeignKey(VisitAnimalHealth, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, verbose_name="farmacos")
    quantity = models.IntegerField("cantidad", default=0)

    class Meta:
        verbose_name = "visita sanidad animal - detalle"
        verbose_name_plural = "visitas sanidad animal - detalles"


class VisitGeneticImprovementVacuno(models.Model):
    checksum = models.CharField(max_length=100, default="")
    visited_at = models.DateField(
        "fecha de visita", blank=True, null=True
    )  # Because current XLS doesn't have all dates
    production_unit = models.ForeignKey(
        ProductionUnit,
        on_delete=models.CASCADE,
        verbose_name="UP",
        blank=True,
        null=True,
    )
    up_member = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_member_animal_vacuno",
        verbose_name="up. integrante",
        null=True,
        blank=True,
    )
    employ_specialist = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_specialist_vacuno",
        verbose_name="personal especialista",
    )
    employ_responsable = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_responsable_vacuno",
        verbose_name="personal responsable",
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name="actividad"
    )
    bull_name = models.CharField("nombre de toro", max_length=30, null=True, blank=True)
    bull_race = models.CharField("raza de toro", max_length=30, null=True, blank=True)
    pajilla_type = models.CharField(
        "tipo pajilla", max_length=30, null=True, blank=True
    )
    pajilla_origin = models.CharField(
        "procedencia pajilla", max_length=30, null=True, blank=True
    )
    pajillas_number = models.IntegerField("nº de pajillas", default=0)
    cow_name = models.CharField("nombre de vaca", max_length=30, null=True, blank=True)
    cow_race = models.CharField("raza de vaca", max_length=30, null=True, blank=True)
    service_number = models.CharField(
        "nº de servicio", max_length=30, null=True, blank=True
    )
    pregnant = models.IntegerField("preñada", default=0)
    empty = models.IntegerField("vacia", default=0)
    birthday = models.CharField("f. nacimiento", max_length=30, null=True, blank=True)
    earring_number = models.CharField(
        "nº de arete", max_length=30, null=True, blank=True
    )
    baby_name = models.CharField("nombre de cria", max_length=30, null=True, blank=True)
    male = models.IntegerField("macho", default=0)
    female = models.IntegerField("hembra", default=0)
    death = models.IntegerField("muerta", default=0)
    baby_bull_name = models.CharField(
        "cria-nombre de toro", max_length=30, null=True, blank=True
    )
    baby_cow_name = models.CharField(
        "cria-nombre de vaca", max_length=30, null=True, blank=True
    )
    male_attendance = models.IntegerField(
        "asis varones capac manejo reproductivo", default=0
    )
    female_attendance = models.IntegerField(
        "asis mujeres capac manejo reproductivo", default=0
    )
    technical_assistance_attendance = models.IntegerField(
        "asis tec manejo ganado vacuno lechero", default=0
    )
    vacunos_number = models.IntegerField("cant vacunos", default=0)

    class Meta:
        verbose_name = "visita MG vacuno"
        verbose_name_plural = "visitas MG vacunos"


class VisitGeneticImprovementOvino(models.Model):
    checksum = models.CharField(max_length=100, default="")
    visited_at = models.DateField(
        "fecha de visita", blank=True, null=True
    )  # Because current XLS doesn't have all dates
    production_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE, verbose_name="UP"
    )
    up_member = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_member_animal_ovino",
        verbose_name="up. integrante",
        null=True,
        blank=True,
    )
    employ_specialist = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_specialist_ovino",
        verbose_name="personal especialista",
    )
    employ_responsable = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_responsable_ovino",
        verbose_name="personal responsable",
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name="actividad"
    )
    selected_ovines = models.IntegerField("ovinos seleccionados", default=0)
    synchronized_ovines = models.IntegerField("ovinos sincronizados", default=0)
    inseminated_sheeps_corriedale = models.IntegerField(
        "ovejas inseminadas corriedale", default=0
    )
    inseminated_sheeps_criollas = models.IntegerField(
        "ovenas inseminadas criollas", default=0
    )
    pregnant = models.IntegerField("preñadas", default=0)
    empty = models.IntegerField("vacías", default=0)
    not_evaluated = models.IntegerField("no evaluadas", default=0)
    baby_males = models.IntegerField("crias machos", default=0)
    baby_females = models.IntegerField("crias hembras", default=0)
    baby_deaths = models.IntegerField("crias muertas", default=0)
    course_male_attendance = models.IntegerField(
        "asis varones curso manejo ovinos", default=0
    )
    course_female_attendance = models.IntegerField(
        "asis mujeres curso manejo ovinos", default=0
    )
    technical_assistance_attendance = models.IntegerField(
        "asis tec producción ganado ovino corriedale", default=0
    )
    ovinos_number = models.IntegerField("cant ovinos", default=0)
    rgc_number = models.CharField("nº RGC", max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "visita MG ovino"
        verbose_name_plural = "visitas MG ovinos"


class VisitGeneticImprovementAlpaca(models.Model):
    checksum = models.CharField(max_length=100, default="")
    visited_at = models.DateField(
        "fecha de visita", blank=True, null=True
    )  # Because current XLS doesn't have all dates
    production_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE, verbose_name="UP"
    )
    up_member = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_member_animal_alpaca",
        verbose_name="up. integrante",
        null=True,
        blank=True,
    )
    employ_specialist = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_specialist_alpaca",
        verbose_name="personal especialista",
    )
    employ_responsable = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employ_responsable_alpaca",
        verbose_name="personal responsable",
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name="actividad"
    )
    hato_number = models.IntegerField("nº de hato", default=0)
    hato_babies_number = models.IntegerField("nº de crias en hato", default=0)
    hato_mothers_number = models.IntegerField("nº de madres en hato", default=0)
    hato_males_number = models.IntegerField("nº de machos en hato", default=0)
    female_alpaca_earring_number = models.CharField(
        "selec nº arete alpaca hembra", max_length=30, null=True, blank=True
    )
    female_alpaca_race = models.CharField(
        "selec raza alpaca hembra", max_length=30, null=True, blank=True
    )
    female_alpaca_color = models.CharField(
        "selec color alpaca hembra", max_length=30, null=True, blank=True
    )
    female_alpaca_age = models.CharField(
        "selec edad alpaca hembra", max_length=30, null=True, blank=True
    )
    female_alpaca_category = models.CharField(
        "selec categoria alpaca hembra", max_length=30, null=True, blank=True
    )
    female_alpaca_total_score = models.IntegerField(
        "selec puntaje total alpaca hembra", default=0
    )
    selected_alpacas_number = models.IntegerField(
        "selec cant alpacas seleccionadas", default=0
    )
    empadre_date = models.DateField("fecha empadre", blank=True, null=True)
    alpacas_empadradas = models.CharField(
        "alpacas empadradas", max_length=30, null=True, blank=True
    )
    alpacas_empadradas_number = models.IntegerField(
        "nº de alpacas empadradas", default=0
    )
    male_empadre_number = models.CharField(
        "nº macho empadre", max_length=30, null=True, blank=True
    )
    second_service_date = models.DateField("fecha 2do servicio", blank=True, null=True)
    second_service_male_number = models.CharField(
        "nº macho 2do servicio", max_length=30, null=True, blank=True
    )
    pregnant = models.IntegerField("preñada", default=0)
    empty = models.IntegerField("vacía", default=0)
    baby_birthday = models.DateField("fecha nacimiento cria", blank=True, null=True)
    baby_earring_number = models.CharField(
        "nº de arete cria", max_length=30, null=True, blank=True
    )
    female_baby = models.IntegerField("cria hembra", default=0)
    male_baby = models.IntegerField("cria macho", default=0)
    mortality_baby = models.IntegerField("mortandad cria", default=0)
    mother_of_baby = models.CharField(
        "madre de cria", max_length=30, null=True, blank=True
    )
    father_of_baby = models.CharField(
        "padre de cria", max_length=30, null=True, blank=True
    )
    training_male_attendance = models.IntegerField("asist varones capac", default=0)
    training_female_attendance = models.IntegerField("asist mujeres capac", default=0)
    technical_assistance_attendance = models.IntegerField(
        "asist tec buenas prácticas manejo alpacas", default=0
    )

    class Meta:
        verbose_name = "visita MG alpaca"
        verbose_name_plural = "visitas MG alpacas"


class VisitComponents(models.Model):
    parte_number = models.IntegerField("nro. parte", default=0)
    year = models.CharField("año", max_length=10, null=True, blank=True)
    visited_at = models.DateField("fecha de visita", blank=True, null=True)
    general_data = models.CharField(
        "datos generales", max_length=10, null=True, blank=True
    )
    production_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE, verbose_name="UP"
    )
    age = models.IntegerField("edad RUP", default=0)
    technical_employee = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="technical_employee",
        verbose_name="técnico de cadenas",
        null=True,
        blank=True,
    )
    specialist_employee = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="specialist_employee",
        verbose_name="especialista de cadenas",
        null=True,
        blank=True,
    )
    trainer_employee = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="trainer_employee",
        verbose_name="capacitador",
        null=True,
        blank=True,
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name="actividad"
    )
    quantity = models.IntegerField("cantidad", default=0)
    certificate_delivery = models.IntegerField(
        "entrega de certificados gestión empresarial", default=0
    )
    pedagogical_process = models.IntegerField(
        "procesos pedagógicos equipo cesem", default=0
    )

    class Meta:
        verbose_name = "visita componente ii y iii"
        verbose_name_plural = "visitas componentes ii y iii"


class FilesChecksum(models.Model):
    created_at = models.DateTimeField("f. creación", auto_created=True, auto_now=True)
    checksum = models.CharField(max_length=100)
    filename = models.TextField("nombre")
    visits = models.IntegerField("visitas", default=0)

    class Meta:
        verbose_name = "Archivo Subido"
        verbose_name_plural = "Archivos Subidos"
        ordering = ("created_at",)


class AnualPeriod(models.Model):
    date_from = models.DateField("fecha de inicio de periodo")
    class Meta:
        verbose_name = "Periodo anual"
        verbose_name_plural = "Periodo anual"
