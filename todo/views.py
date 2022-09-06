from django.shortcuts import render, redirect
import datetime
from todo.forms import TodoModelForm
from todo.models import Todo

app_name="todo"

def todo(request):
    
    form = TodoModelForm()
    todos = Todo.objects.all()

    if request.method == "POST":
        form = TodoModelForm(request.POST)
        if form.is_valid():
            current_user=request.user
            print(current_user.id)
            form.save()
            return redirect("todo")
        else:
            print("the form is invlaid")
    
    context = {
        "todos": todos,
        "form":form,
    }

    return render(request, "todo/todo.html", context=context)
