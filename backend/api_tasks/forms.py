from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=[
            'id',
            'title',
            'date_start',
            'date_end', 
            'location',
            'owner',
            'description',
            'status'
        ]