# teacherportal/forms.py
from django import forms
from .models import Attendance
from studentportal.models import Student
from .models import Resource

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'is_present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }



class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file']
