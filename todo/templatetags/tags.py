import datetime
from ipaddress import ip_address
from telnetlib import IP

import geocoder
import requests
import os
from math import trunc
from django import template
import reverse_geocoder as rg
import pycountry


register = template.Library()

'''test'''
ip_a = []

@register.simple_tag
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
        if len(ip_a):
            ip_a.clear()
            ip_a.append(ip)
        else:
            ip_a.append(ip)
        print(f"ip_a1 insde is {ip_a[0]}")
    else:
        ip = request.META.get('REMOTE_ADDR')
        if len(ip_a):
            ip_a.clear()
            ip_a.append(ip)
        else:
            ip_a.append(ip)
        print(f"ip_a2 outside is {ip_a[0]}")
    return ip


print(f"ip_1 outside is {ip_a}")

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

@register.simple_tag
def get_location(request):
    # ip_address = get_ip()
    # print(ip_address)
    original_ip = ip()
    print(f"Original IP is {original_ip}")
    ip_address = ip2long(original_ip)

    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

import socket, struct
import netaddr

#Convert IP string to Int
def ip2long(ip):
    """
    Convert an IP string to long
    """
    # packedIP = socket.inet_aton(ip)
    # return struct.unpack("!L", packedIP)[0]
    print(f"NETAADR is {netaddr.IPAddress(ip)}")
    return netaddr.IPAddress(ip)

def ip():
    if len(ip_a):
        ip = ip_a[0]
        print(f"IP1 is {ip}")
    else:
        ip="8.8.8.8"
        # ip = 2iplong(original_ip)
        print(f"IP2 is {ip}")
    return ip

client_ip = ip()
print(f"Client_IP is {type(client_ip)}")


API_KEY=os.getenv("API_KEY")
G_API_KEY=os.getenv("G_API_KEY")
g = geocoder.ip(client_ip)

print(f"g is {g}.")
# print(f"get_ip is {get_ip()}")
# print(f"get_location is {get_location()}")

lat=g.latlng[0]
lon=g.latlng[1]
COORDINATES = (lat, lon)
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


def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    iso3166_1_alpha_2=result[0]['cc']
    pycountry_result = pycountry.countries.get(alpha_2=iso3166_1_alpha_2)
    return pycountry_result.name
    


