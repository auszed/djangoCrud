from django.contrib import admin
from .models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    """va a permitir ver la creation"""
    readonly_fields = ('created_at',)

# bring the models to edit in the admin
admin.site.register(Task, TaskAdmin )

