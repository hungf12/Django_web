from django import template

register = template.Library()

@register.filter
def currency(value):
    try:
        value = int(float(value))  # Chuyển thành số nguyên
        return "{:,.0f}".format(value).replace(",", ".")  # Dùng dấu "." cho VND
    except ValueError:
        return value

