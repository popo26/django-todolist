from django import template
import datetime

register = template.Library()



@register.simple_tag
def today(request):
    TODAY = datetime.date.today()
    return TODAY