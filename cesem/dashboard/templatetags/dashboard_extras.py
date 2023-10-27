import locale
from datetime import datetime
from django import template
from django.template import loader

register = template.Library()


@register.filter
def get_columns_labels(view_model, colums):
    columns = []
    for column in colums:
        columns.append(view_model.get_serializer().fields[column].label)
    return columns


@register.filter
def get_column_label(view_model, column_name):        
    if column_name in view_model.get_serializer().fields:
        return view_model.get_serializer().fields[column_name].label
    return column_name

@register.filter
def get_is_hidden(view_model, column_name):
    meta = view_model.get_serializer().Meta
    if 'custom_kwargs' in meta.__dict__:
        custom_kwargs = meta.custom_kwargs
        if custom_kwargs:
            if column_name in custom_kwargs:
                if 'hidden' in custom_kwargs[column_name]:
                    return True
    return False


@register.filter
def get_home_path(value):
    return value.get_serializer().get_home_path()


@register.filter
def get_model_name_plural(value):
    return value.get_serializer().Meta.model._meta.verbose_name_plural.title()


@register.filter
def get_model_name(value):
    return value.get_serializer().Meta.model._meta.verbose_name.title()

def get_count_position_points(activity):
    letters = list(activity.position)
    points = filter(lambda letter: letter == ".", letters)
    points = list(points)
    points = len(points)
    return points

@register.simple_tag
def get_activity_class(activity):
    points = get_count_position_points(activity)
    if points == 0:
        return "component"
    if points == 1:
        return "activity"
    if points == 2:
        return "sub-activity"
    return ""


@register.simple_tag
def get_activity_data_value(activity, index_name, activities_data):
    try:
        int(activity.position)  # is Principal actitivy
        return ""
    except:
        activity_id = activity.id
        if activity_id in activities_data:
            if index_name in activities_data[activity_id]:
                return activities_data[activity_id][index_name]
        points = get_count_position_points(activity)
        if points < 2:
            return ''
        return 0

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_meta(activity, year):
    if year == 2022:
        return activity.meta_2022    
    if year == 2023:
        return activity.meta_2023    
    if year == 2024:
        return activity.meta_2024
    return '{} no configurado, consultar con el administrador'.format(year)    


@register.simple_tag
def get_activity_progress_value(year, activity, activities_data):
    try:
        value = activities_data[activity.id]
        meta = get_meta(activity, year)
        result = (value/meta)*100
        result = '{}%'.format(str(round(result, 2)))
        return result
    except:
        return 0

@register.simple_tag
def get_activity_data_zone_value(activity, zone, activities_data):
    try:
        int(activity.position)  # is Principal actitivy
        return ""
    except:
        activity_id = activity.id
        if activity_id in activities_data:
            if zone.id in activities_data[activity_id]:
                return activities_data[activity_id][zone.id]
        return 0


@register.filter
def get_start_date_of_week(week_number, year):
    start_of_week = datetime.strptime(f"{year}-W{week_number}-1", "%Y-W%W-%w").date()
    return start_of_week


@register.filter
def get_month(month_number):
    months_names = [
        'enero',
        'febrero',
        'marzo',
        'abril',
        'mayo',
        'junio',
        'julio',
        'agosto',
        'septiembre',
        'octubre',
        'noviembre',
        'diciembre'
    ]

    return months_names[month_number - 1]


@register.filter
def active_if_path_match(keyword, request):
    if request.path.__contains__(keyword):
        return "active"
    return ""

    # @register.filter
    # def format_custom_value(value):
    #    if value is None or isinstance(value, bool):
    #        return "%s" % {True: "Si", False: "No", None: "ninguno"}[value]
    # if isinstance(value, list):
    #    if any(isinstance(item, (list, dict)) for item in value):
    #        template = loader.get_template("rest_framework/admin/list.html")
    #        context = {
    # "view": VisitAnimalHealthViewSet,
    #           "value": value,
    # "columns": ["visited_at", "cesem_especialista", "diagnostico"],
    #        }
    #    return template.render(context)

    return value


from django.utils.safestring import mark_safe
from django.utils.html import escape, format_html, smart_urlquote


@register.filter
def format_custom_value(value):
    if getattr(value, "is_hyperlink", False):
        name = str(value.obj)
        return mark_safe("<a href=%s>%s</a>" % (value, escape(name)))
    if value is None or isinstance(value, bool) or value == "True" or value == "False":
        if value == "True" or value == "False":
            value = value == "True"
        return mark_safe(
            "<code>%s</code>" % {True: "Si", False: "No", None: "-"}[value]
        )
    elif isinstance(value, list):
        if any(isinstance(item, (list, dict)) for item in value):
            template = loader.get_template("rest_framework/admin/list_value.html")
            template = loader.get_template("rest_framework/admin/list_simple.html")
        else:
            template = loader.get_template(
                "rest_framework/admin/simple_list_value.html"
            )
        data = value.serializer._data
        columns = []
        if len(data) > 0:
            for key, val in data[0].items():
                if key != "url":
                    columns.append(key)
            context = {"results": value, "columns": columns}
        else:
            context = {"value": value}
        return template.render(context)
    elif isinstance(value, dict):
        template = loader.get_template("rest_framework/admin/dict_value.html")
        context = {"value": value}
        return template.render(context)
    elif isinstance(value, str):
        if (
            value.startswith("http:")
            or value.startswith("https:")
            or value.startswith("/")
        ) and not re.search(r"\s", value):
            return mark_safe(
                '<a href="{value}">{value}</a>'.format(value=escape(value))
            )
        elif "@" in value and not re.search(r"\s", value):
            return mark_safe(
                '<a href="mailto:{value}">{value}</a>'.format(value=escape(value))
            )
        elif "\n" in value:
            return mark_safe("<pre>%s</pre>" % escape(value))
    return str(value)
