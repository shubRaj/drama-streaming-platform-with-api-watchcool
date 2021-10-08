from django import template
register = template.Library()
@register.filter(name="getClassName")
def getClassName(value):
    return value.__class__.__name__