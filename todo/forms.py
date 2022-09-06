
from django import forms

from todo.models import Todo

class TodoModelForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = "__all__"
        
