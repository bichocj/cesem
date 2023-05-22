# Generated by Django 4.2 on 2023-05-18 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Activity",
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
                ("position", models.CharField(max_length=6, verbose_name="posición")),
                ("name", models.CharField(max_length=100, verbose_name="nombre")),
                (
                    "short_name",
                    models.CharField(
                        default="", max_length=100, verbose_name="nombre corto"
                    ),
                ),
                (
                    "um",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="unidad de medida",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.activity",
                        verbose_name="actividad superior",
                    ),
                ),
            ],
            options={
                "verbose_name": "actividad",
                "verbose_name_plural": "actividades",
                "ordering": ("position",),
            },
        ),
        migrations.CreateModel(
            name="Community",
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
                    "name",
                    models.CharField(max_length=20, unique=True, verbose_name="nombre"),
                ),
            ],
            options={
                "verbose_name": "comunidad",
                "verbose_name_plural": "comunidades",
            },
        ),
        migrations.CreateModel(
            name="Diagnostic",
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
                ("name", models.CharField(max_length=50, verbose_name="observación")),
            ],
            options={
                "verbose_name": "diagnostico",
                "verbose_name_plural": "diagnosticos",
            },
        ),
        migrations.CreateModel(
            name="Drug",
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
                ("name", models.CharField(max_length=50, verbose_name="nombre")),
                (
                    "um",
                    models.IntegerField(
                        choices=[(0, "ml."), (1, "gr.")],
                        default=0,
                        verbose_name="unidad de medida",
                    ),
                ),
            ],
            options={
                "verbose_name": "farmaco",
                "verbose_name_plural": "farmacos",
            },
        ),
        migrations.CreateModel(
            name="Person",
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
                    "dni",
                    models.CharField(
                        blank=True, max_length=8, null=True, verbose_name="dni"
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="nombres")),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="apellidos"
                    ),
                ),
                (
                    "sex",
                    models.IntegerField(
                        blank=True,
                        choices=[(0, "femenino"), (1, "masculino")],
                        null=True,
                        verbose_name="sexo",
                    ),
                ),
                (
                    "title",
                    models.IntegerField(
                        blank=True,
                        choices=[(0, "tec."), (1, "mvz.")],
                        null=True,
                        verbose_name="titulo",
                    ),
                ),
            ],
            options={
                "verbose_name": "persona",
                "verbose_name_plural": "personas",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ProductionUnit",
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
                ("tipology", models.IntegerField(default=0)),
                ("is_pilot", models.BooleanField(default=False)),
                (
                    "community",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.community",
                        verbose_name="comunidad",
                    ),
                ),
                (
                    "person_member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="person_member_animal",
                        to="core.person",
                        verbose_name="up. integrante",
                    ),
                ),
                (
                    "person_responsable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="person_responsable_animal",
                        to="core.person",
                        verbose_name="up. responsable",
                    ),
                ),
            ],
            options={
                "verbose_name": "Unidad de Producción",
                "verbose_name_plural": "Unidades de Producción",
            },
        ),
        migrations.CreateModel(
            name="SicknessObservation",
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
                ("name", models.CharField(max_length=50, verbose_name="nombre")),
            ],
            options={
                "verbose_name": "enfermedad/observación",
                "verbose_name_plural": "enfermedades/observaciones",
            },
        ),
        migrations.CreateModel(
            name="VisitAnimal",
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
                    "visited_at",
                    models.DateField(
                        blank=True, null=True, verbose_name="fecha de creación"
                    ),
                ),
                ("cattle", models.IntegerField(default=0, verbose_name="vacunos")),
                ("sheep", models.IntegerField(default=0, verbose_name="ovinos")),
                ("alpacas", models.IntegerField(default=0, verbose_name="alpacas")),
                ("llamas", models.IntegerField(default=0, verbose_name="llamas")),
                ("canes", models.IntegerField(default=0, verbose_name="canes")),
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
                        related_name="employ_responsable_animal",
                        to="core.person",
                        verbose_name="personal responsable",
                    ),
                ),
                (
                    "employ_specialist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employ_specialist_animal",
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
                "verbose_name": "visita animal",
                "verbose_name_plural": "visitas animales",
            },
        ),
        migrations.CreateModel(
            name="Zone",
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
                    "name",
                    models.CharField(max_length=20, unique=True, verbose_name="nombre"),
                ),
            ],
            options={
                "verbose_name": "zona",
                "verbose_name_plural": "zonas",
            },
        ),
        migrations.CreateModel(
            name="VisitGrass",
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
                ("visited_at", models.DateField(verbose_name="fecha de creacion")),
                (
                    "utm_coordenate",
                    models.CharField(
                        blank=True,
                        max_length=30,
                        null=True,
                        verbose_name="coordenadas UTM anuales",
                    ),
                ),
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
                    "employ_responsable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employ_responsable_grass",
                        to="core.person",
                        verbose_name="personal responsable",
                    ),
                ),
                (
                    "employ_specialist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employ_specialist_grass",
                        to="core.person",
                        verbose_name="personal especialista",
                    ),
                ),
                (
                    "production_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.productionunit",
                    ),
                ),
            ],
            options={
                "verbose_name": "visita pastos",
                "verbose_name_plural": "visitas pastos",
            },
        ),
        migrations.CreateModel(
            name="VisitAnimalDetails",
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
                ("quantity", models.IntegerField(default=0, verbose_name="cantidad")),
                (
                    "drug",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.drug",
                        verbose_name="farmacos",
                    ),
                ),
                (
                    "visit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.visitanimal",
                    ),
                ),
            ],
            options={
                "verbose_name": "visita animal - detalle",
                "verbose_name_plural": "visitas animales - detalles",
            },
        ),
        migrations.CreateModel(
            name="Sector",
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
                    "name",
                    models.CharField(max_length=20, unique=True, verbose_name="nombre"),
                ),
                (
                    "community",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.community",
                        verbose_name="comunidad",
                    ),
                ),
            ],
            options={
                "verbose_name": "sector",
                "verbose_name_plural": "sectores",
            },
        ),
        migrations.AddField(
            model_name="productionunit",
            name="sector",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.sector",
                verbose_name="sector",
            ),
        ),
        migrations.AddField(
            model_name="productionunit",
            name="zone",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.zone",
                verbose_name="zona",
            ),
        ),
        migrations.AddField(
            model_name="community",
            name="zone",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.zone",
                verbose_name="zona",
            ),
        ),
    ]
