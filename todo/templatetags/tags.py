import datetime
import geocoder
import requests
import os
from math import trunc
from django import template
import reverse_geocoder as rg
import pycountry


register = template.Library()

'''test'''

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

@register.simple_tag
def get_location(request):
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data



ip = get_ip()

API_KEY=os.getenv("API_KEY")
G_API_KEY=os.getenv("G_API_KEY")
g = geocoder.ip(ip)

print(f"g is {g}.")
# print(f"get_ip is {get_ip()}")
# print(f"get_location is {get_location()}")

lat=g.latlng[0]
lon=g.latlng[1]
COORDINATES = (lat, lon)
weather_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
geocoder_URL=f'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en'

@register.simple_tag
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




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


def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    iso3166_1_alpha_2=result[0]['cc']
    pycountry_result = pycountry.countries.get(alpha_2=iso3166_1_alpha_2)
    return pycountry_result.name
    


