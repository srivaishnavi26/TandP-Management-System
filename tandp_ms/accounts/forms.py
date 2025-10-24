from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'full_name', 'phone', 'graduation_year', 'resume', 'department']
        widgets = {
            'department': forms.TextInput(attrs={'readonly': 'readonly'}),  # department auto-assigned
        }
