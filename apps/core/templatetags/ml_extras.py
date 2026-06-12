from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return ''


@register.filter
def divide_by(value, arg):
    try:
        return float(value) / float(arg)
    except (TypeError, ValueError, ZeroDivisionError):
        return ''


@register.filter
def getattr_filter(obj, attr):
    try:
        return getattr(obj, attr)
    except AttributeError:
        return ''


# Register with the name 'getattr' so templates can use |getattr
register.filter('getattr', getattr_filter)
