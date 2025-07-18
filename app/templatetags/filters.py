from django import template

register = template.Library()

@register.filter
def currency(value):
    try:
        value = float(value)
        return f"{value:,.0f}"
    except:
        return value
