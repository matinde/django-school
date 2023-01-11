# create modelforms
from django import forms
from django_school.models import Student
from django_school.models import Teacher
from django_school.models import Parent
from django_school.models import Classroom
from django_school.models import Exam
from django_school.models import Subject
from django_school.models import Announcements
from django_school.models import Assignment

class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs = {'class': 'input',}
        self.fields['last_name'].widget.attrs = {'class': 'input',}
        self.fields['current_status'].widget.attrs = {'class': 'input',}
        self.fields['registration_number'].widget.attrs = {'class': 'input',}
        self.fields['admission_date'].widget.attrs = {'class': 'input',}
        self.fields['photo'].widget.attrs = {'class': 'input',}
        self.fields['school'].widget.attrs = {'class': 'input',}
        self.fields['grade'].widget.attrs = {'class': 'input',}
        self.fields['classroom'].widget.attrs = {'class': 'input',}
        self.fields['date_of_birth'].widget.attrs = {'class': 'input',}
        
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "current_status", "registration_number", 
                    "admission_date", "photo", "school", "grade", "classroom", "date_of_birth",]

   

            
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

class AnnouncementsForm(forms.ModelForm):
    class Meta:
        model = Announcements
        fields = "__all__"

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = "__all__"