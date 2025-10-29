from django import template

register = template.Library()

@register.filter
def get_field_value(obj, field_name):
    """Return dynamic attribute value of an object by name"""
    return getattr(obj, field_name, None)

@register.filter
def get_attr(obj, attr):
    """Permet d'accéder dynamiquement à un attribut d'un objet dans le template"""
    return getattr(obj, attr, None)
