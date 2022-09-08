from django import template
import datetime

register = template.Library()


@register.simple_tag
def today(request):
    TODAY = datetime.date.today()
    nicer_format=TODAY.strftime('%a %d %b %Y')
    return nicer_format

@register.simple_tag
def time(request):
    now = datetime.datetime.now()
    time = now.strftime("%I:%M %p")
    return time