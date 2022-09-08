import datetime
import geocoder
import requests
import os
from math import trunc
from django import template

register = template.Library()

API_KEY=os.getenv("API_KEY")
G_API_KEY=os.getenv("G_API_KEY")
g = geocoder.ip('me')

lat=g.latlng[0]
lon=g.latlng[1]
weather_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
geocoder_URL=f'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en'

@register.simple_tag
def geo_name(request):
    response=requests.get(geocoder_URL)
    data=response.json()
    loc=data['localityInfo']['administrative'][2]['name']
    return loc

@register.simple_tag
def weather_api(request):
    response = requests.get(weather_URL)
    data=response.json()
    current_weather = data["weather"][0]['description']
    return current_weather

@register.simple_tag
def temp_api(request):
    response = requests.get(weather_URL)
    data=response.json()
    current_temp = trunc(data['main']["temp"])
    return current_temp

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

