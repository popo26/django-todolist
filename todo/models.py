from django.db import models

class Todo(models.Model):
    todo = models.CharField(max_length=200, null=False)
    date = models.DateField()

    def __str__(self):
        return self.todo
