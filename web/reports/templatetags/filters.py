from django import template



register = template.Library()



@register.filter
def money(value, scale):
    return '${:,d}'.format(value / scale)
