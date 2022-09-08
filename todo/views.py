
from django.shortcuts import render, redirect
import datetime
# from todo.forms import TodoModelForm
from todo.models import Todo

import calendar
from calendar import HTMLCalendar

from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm
from django.views.generic.edit import DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
  

app_name="todo"


# def todo(request, year, month):
    
#     form = TodoModelForm()
#     todos = Todo.objects.all()

#     month = month.capitalize()
#     month_number = list(calendar.month_name).index(month)
#     month_number = int(month_number)
#     cal = HTMLCalendar().formatmonth(year, month_number)
  
#     if request.method == "POST":
#         form = TodoModelForm(request.POST)
#         if form.is_valid():
#             current_user=request.user
#             print(current_user.id)
#             print(current_user.username)
#             form.save()
#             return redirect("todo")
#         else:
#             print("the form is invlaid")
    
#     context = {
#         "todos": todos,
#         "form":form,
#         "year":year, 
#         'month':month,
#         "month_number": month_number,
#         "cal":cal,
                
#     }

#     return render(request, "todo/todo.html", context=context)

# def test(request, year, month):
#     name = "Ai"
#     month = month.capitalize()
#     month_number = list(calendar.month_name).index(month)
#     month_number = int(month_number)

#     cal = HTMLCalendar().formatmonth(year, month_number)
#     context={
#         "name":name, 
#         "year":year, 
#         'month':month,
#         "month_number": month_number,
#         "cal":cal,
#     }
#     return render(request, "todo/test.html", context=context)

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
    


