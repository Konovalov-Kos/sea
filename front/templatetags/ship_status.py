from django import template

register = template.Library()

@register.filter
def ship_status(val):
    if val == 0:
        return "   "
    if val == 1:
        return " . "
    if val == 2:
        return " * "
    if val == 3:
        return " }{ "
    return val