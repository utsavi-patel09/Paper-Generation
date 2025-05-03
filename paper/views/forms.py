from django import forms
from paper.models.teacher import Teacher

class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'phone', 'email', 'profile_picture']
