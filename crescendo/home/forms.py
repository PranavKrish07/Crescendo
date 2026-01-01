from django import forms
from .models import List, Task

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name']
        labels = {
            'name': '',
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task']
        labels = {
            'task': '',
        }