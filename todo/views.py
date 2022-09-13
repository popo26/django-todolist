
import calendar
import datetime
import calendar
import requests
from datetime import timedelta
from django.shortcuts import render, redirect
from todo.models import Todo
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe

from todo.templatetags.tags import COORDINATES
from .models import *
from .utils import Calendar
from .forms import EventForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .templatetags.tags import reverseGeocode
  

app_name="todo"

#To use dictionary as template variable
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# def get_user(request):
#     current_user = request.user
#     return current_user.username


#Login/Logout counters added because request.user doesn't work outside views.py
@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    current_user = request.user
    print(current_user)
    print(f"LoginStatus is {current_user.login_status}")
    current_user.login_status = True
    current_user.save()
    print(f"LoginStatus is{current_user.login_status}")
    if current_user.logout_status == True:
        current_user.logout_status = False
        current_user.save()
    print(f"LogOut Status is {current_user.logout_status}")
    print('User Just logged In....')
    
@receiver(user_logged_out)
def on_logout(sender, user, request, **kwargs):
    current_user = request.user
    current_user.logout_status = True
    current_user.login_status = False
    current_user.save()
    print(f"LoginStatus is {current_user.login_status}")
    print(f"LogOut Status is {current_user.logout_status}")
    print('User Just logged Out....')


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'todo/todo.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        now = datetime.now()
        current_user=self.request.user
        name=current_user.username
        todos = Event.objects.filter(start_time__year=now.year, start_time__month=now.month, start_time__day=now.strftime('%d'), user_name=name)
        
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['todos'] = todos
        context['current_user'] = name
  
        if self.request.method == "POST":
            todo = self.request.POST.get['delete-todo']
            delete_todo = Event.object.get(id=todo.id)
            delete_todo.delete()
        
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance, initial={"user_name":request.user.username})
    if request.POST and form.is_valid():
        current_user = request.user
        form.user_name = current_user.username
        form.save()
        return HttpResponseRedirect(reverse('todo:calendar'))
    return render(request, 'todo/event.html', {'form': form})

class EventDeleteView(LoginRequiredMixin,DeleteView):
    model = Event
    success_url = reverse_lazy("todo:calendar")

def covid(request):
    today = datetime.today()
    y3 = today - timedelta(days=3)
    two_days_before_yesterday = y3.strftime('%Y-%m-%d')
    y2 = today - timedelta(days=2)
    day_before_yesterday = y2.strftime('%Y-%m-%d')

    country = reverseGeocode(coordinates=COORDINATES).lower()
    country_name = country.replace(" ", "-")
   
    covid_url = f"https://api.covid19api.com/total/country/{country_name}/status/confirmed?from={two_days_before_yesterday}T00:00:00Z&to={day_before_yesterday}T00:00:00Z"
    response=requests.get(covid_url)
    data=response.json()
    
    two_days_before_yesterday_cases = int(data[1]['Cases'])
    day_before_yesterday_cases = int(data[0]['Cases'])
    confirmed_cases_till_now = two_days_before_yesterday_cases - day_before_yesterday_cases
    print(confirmed_cases_till_now)

    context = {
        'country_name': country,
        "confirmed_cases_till_now" : confirmed_cases_till_now,
        "two_days_before_yesterday": two_days_before_yesterday,
        "day_before_yesterday": day_before_yesterday,
    }
    
    return render(request, 'todo/covid.html', context=context)
    
def fun_facts(request):
    
    return render(request, 'todo/fun_facts.html')

 