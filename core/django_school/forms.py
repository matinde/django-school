# create modelforms
from django import forms
from django_school.models import Student
from django_school.models import Teacher
from django_school.models import Parent
from django_school.models import Classroom
from django_school.models import Exam
from django_school.models import Subject

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = "__all__"

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = "__all__"

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"
