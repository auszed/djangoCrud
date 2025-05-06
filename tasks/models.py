from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)

    # una llave para otra tablas
    # CASCADE = cuando se elimina el usuario se eliminan todas sus tareas
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' -by ' + self.user.username