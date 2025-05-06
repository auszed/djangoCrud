from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

        # asi se pasan las classes personalizadas
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto text-center'}),
        }
