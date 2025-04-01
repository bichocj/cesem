# Generated by Django 4.2 on 2025-03-13 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0036_productionunit_created_at_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="VisitAnimalDeworming",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_created=True, auto_now=True, verbose_name="f. creación"
                    ),
                ),
                ("checksum", models.CharField(default="", max_length=100)),
                (
                    "visited_at",
                    models.DateField(
                        blank=True, null=True, verbose_name="fecha de visita"
                    ),
                ),
                (
                    "up_member_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        null=True,
                        verbose_name="UP integrante",
                    ),
                ),
                (
                    "up_member_dni",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=20,
                        null=True,
                        verbose_name="N dni",
                    ),
                ),
                (
                    "sex",
                    models.IntegerField(
                        blank=True,
                        choices=[(0, "femenino"), (1, "masculino")],
                        null=True,
                        verbose_name="sexo IUP",
                    ),
                ),
                (
                    "v_race",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        null=True,
                        verbose_name="vacunos raza",
                    ),
                ),
                (
                    "v_dewormed",
                    models.IntegerField(
                        default=0, verbose_name="vacunos desparasitados"
                    ),
                ),
                (
                    "v_no_dewormed",
                    models.IntegerField(
                        default=0, verbose_name="vacunos no desparasitados"
                    ),
                ),
                (
                    "v_total",
                    models.IntegerField(default=0, verbose_name="total vacunos"),
                ),
                (
                    "o_race",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        null=True,
                        verbose_name="ovinos raza",
                    ),
                ),
                (
                    "o_dewormed",
                    models.IntegerField(
                        default=0, verbose_name="ovinos desparasitados"
                    ),
                ),
                (
                    "o_no_dewormed",
                    models.IntegerField(
                        default=0, verbose_name="ovinos no desparasitados"
                    ),
                ),
                (
                    "o_total",
                    models.IntegerField(default=0, verbose_name="total ovinos"),
                ),
                (
                    "a_race",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        null=True,
                        verbose_name="alpacas raza",
                    ),
                ),
                (
                    "a_dewormed",
                    models.IntegerField(
                        default=0, verbose_name="alpacas desparasitados"
                    ),
                ),
                (
                    "a_no_dewormed",
                    models.IntegerField(
                        default=0, verbose_name="alpacas no desparasitados"
                    ),
                ),
                (
                    "a_total",
                    models.IntegerField(default=0, verbose_name="total alpacas"),
                ),
                (
                    "l_race",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        null=True,
                        verbose_name="llamas raza",
                    ),
                ),
                (
                    "l_dewormed",
                    models.IntegerField(
                        default=0, verbose_name="llamas desparasitados"
                    ),
                ),
                (
                    "l_no_dewormed",
                    models.IntegerField(
                        default=0, verbose_name="llamas no desparasitados"
                    ),
                ),
                (
                    "l_total",
                    models.IntegerField(default=0, verbose_name="total llamas"),
                ),
                ("c_total", models.IntegerField(default=0, verbose_name="total canes")),
                ("total", models.IntegerField(default=0, verbose_name="total")),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.activity",
                        verbose_name="actividad",
                    ),
                ),
                (
                    "diagnostic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.diagnostic",
                        verbose_name="diagnostico",
                    ),
                ),
                (
                    "employ_responsable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employ_responsable_deworming",
                        to="core.person",
                        verbose_name="personal responsable",
                    ),
                ),
                (
                    "employ_specialist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employ_specialist_deworming",
                        to="core.person",
                        verbose_name="personal especialista",
                    ),
                ),
                (
                    "production_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.productionunit",
                        verbose_name="UP",
                    ),
                ),
                (
                    "sickness_observation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.sicknessobservation",
                        verbose_name="enfermedad/observación",
                    ),
                ),
            ],
            options={
                "verbose_name": "visita vacunacion",
                "verbose_name_plural": "visitas vacunacion",
                "ordering": ("visited_at", "production_unit"),
            },
        ),
        migrations.CreateModel(
            name="VisitComponent2",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "parte_number",
                    models.IntegerField(default=0, verbose_name="nro. parte"),
                ),
                (
                    "month_f",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="mes"
                    ),
                ),
                (
                    "visited_at",
                    models.DateField(
                        blank=True, null=True, verbose_name="fecha de visita"
                    ),
                ),
                (
                    "general_data",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="datos generales",
                    ),
                ),
                ("age", models.IntegerField(default=0, verbose_name="edad RUP")),
                ("quantity", models.IntegerField(default=0, verbose_name="cantidad")),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.activity",
                        verbose_name="actividad",
                    ),
                ),
                (
                    "production_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.productionunit",
                        verbose_name="UP",
                    ),
                ),
                (
                    "specialist_employee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specialist_employee_c2",
                        to="core.person",
                        verbose_name="especialista de cadenas",
                    ),
                ),
                (
                    "technical_employee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="technical_employee_c2",
                        to="core.person",
                        verbose_name="técnico de cadenas",
                    ),
                ),
                (
                    "trainer_employee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trainer_employee_c2",
                        to="core.person",
                        verbose_name="capacitador",
                    ),
                ),
            ],
            options={
                "verbose_name": "visita componente ii",
                "verbose_name_plural": "visitas componente ii",
            },
        ),
        migrations.CreateModel(
            name="VisitComponent3",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_created=True, auto_now=True, verbose_name="f. creación"
                    ),
                ),
                (
                    "parte_number",
                    models.IntegerField(default=0, verbose_name="nro. parte"),
                ),
                (
                    "month_f",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="mes"
                    ),
                ),
                (
                    "visited_at",
                    models.DateField(
                        blank=True, null=True, verbose_name="fecha de visita"
                    ),
                ),
                (
                    "general_data",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="datos generales",
                    ),
                ),
                ("age", models.IntegerField(default=0, verbose_name="edad RUP")),
                ("quantity", models.IntegerField(default=0, verbose_name="cantidad")),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.activity",
                        verbose_name="actividad",
                    ),
                ),
                (
                    "production_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.productionunit",
                        verbose_name="UP",
                    ),
                ),
                (
                    "specialist_employee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specialist_employee_c3",
                        to="core.person",
                        verbose_name="especialista de cadenas",
                    ),
                ),
                (
                    "technical_employee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="technical_employee_c3",
                        to="core.person",
                        verbose_name="técnico de cadenas",
                    ),
                ),
                (
                    "trainer_employee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trainer_employee_c3",
                        to="core.person",
                        verbose_name="capacitador",
                    ),
                ),
            ],
            options={
                "verbose_name": "visita componente iii",
                "verbose_name_plural": "visitas componente iii",
            },
        ),
        migrations.AlterField(
            model_name="visitanimalhealth",
            name="diagnostic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.diagnostic",
                verbose_name="diagnostico",
            ),
        ),
        migrations.AlterField(
            model_name="visitanimalhealth",
            name="sickness_observation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.sicknessobservation",
                verbose_name="enfermedad/observación",
            ),
        ),
        migrations.DeleteModel(
            name="VisitComponents",
        ),
    ]
