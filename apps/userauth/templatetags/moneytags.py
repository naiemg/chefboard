from django import template
register = template.Library()

def print_dollar_amount(value):
    try:
        return format(value/100, '.2f')
    except (ValueError, ZeroDivisionError):
        return None

register.filter(print_dollar_amount)