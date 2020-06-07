from django import forms
from .models import Tasks


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = '__all__'
        exclude = ['created_by', 'updated_by', 'added_at']