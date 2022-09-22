from django.db import models
from django.urls import reverse
from accounts.models import CustomUser

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user_name = models.CharField(max_length=50)
    username = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)

    @property
    def get_html_url(self):
        url = reverse('todo:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} ({self.user_name})</a>'

    @property
    def get_event_name(self):
        url = reverse('todo:event_edit', args=(self.id,))
        return f'{self.title} ({self.user_name})'

    @property
    def get_user_id(self):
        user = self.request.session['_auth_user_id']
        return user.id


class Todo(models.Model):
    todo = models.CharField(max_length=200, null=False)
    date = models.DateField()

    def __str__(self):
        return self.todo
