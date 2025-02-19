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
from django_school.models import Grade

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

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs = {'class': 'input',}
        self.fields['last_name'].widget.attrs = {'class': 'input',}
        self.fields['current_status'].widget.attrs = {'class': 'input',}
        self.fields['gender'].widget.attrs = {'class': 'input',}
        self.fields['photo'].widget.attrs = {'class': 'input',}
        self.fields['school'].widget.attrs = {'class': 'input',}
        self.fields['email'].widget.attrs = {'class': 'input',}
        self.fields['phone_numbers'].widget.attrs = {'class': 'input',}
        self.fields['department'].widget.attrs = {'class': 'input',}
        
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "current_status","gender", "photo", "school", "email", "phone_numbers", "department",]

class ParentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs = {'class': 'input',}
        self.fields['last_name'].widget.attrs = {'class': 'input',}
        self.fields['email'].widget.attrs = {'class': 'input',}
        self.fields['phone_numbers'].widget.attrs = {'class': 'input',}

    class Meta:
        model = Parent
        fields = ["first_name", "last_name", "email", "phone_numbers",]

class ClassroomForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClassroomForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs = {'class': 'input',}
        
    class Meta:
        model = Classroom
        fields = ['name',]

class GradeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs = {'class': 'input',}
        self.fields['subjects'].widget.attrs = {'class': 'input',}

    class Meta:
        model = Grade
        fields = ['name', 'subjects',]

class ExamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs = {'class': 'input',}
        self.fields['year'].widget.attrs = {'class': 'input',}
        self.fields['month'].widget.attrs = {'class': 'input',}
        self.fields['day'].widget.attrs = {'class': 'input',}
        self.fields['term'].widget.attrs = {'class': 'input',}
     
    class Meta:
        model = Exam
        fields = ['name', 'year', 'month', 'day', 'term',]

class SubjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs = {'class': 'input',}
        self.fields['teacher'].widget.attrs = {'class': 'input',}
        self.fields['description'].widget.attrs = {'class': 'input',}
        self.fields['duration'].widget.attrs = {'class': 'input',}
        self.fields['exam_results'].widget.attrs = {'class': 'input',}
      
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'description', 'duration', 'exam_results',]

class AnnouncementsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnnouncementsForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs = {'class': 'input',}
        self.fields['description'].widget.attrs = {'class': 'input',}
        self.fields['grade'].widget.attrs = {'class': 'input',}
        self.fields['date'].widget.attrs = {'class': 'input',}
        
    class Meta:
        model = Announcements
        fields = ['title', 'description', 'grade', 'date',]

class AssignmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs = {'class': 'input',}
        self.fields['description'].widget.attrs = {'class': 'input',}
        self.fields['grade'].widget.attrs = {'class': 'input',}
        self.fields['subject'].widget.attrs = {'class': 'input',}
        self.fields['classroom'].widget.attrs = {'class': 'input',}
        self.fields['created_date'].widget.attrs = {'class': 'input',}
        self.fields['due_date'].widget.attrs = {'class': 'input',}
        self.fields['created_by'].widget.attrs = {'class': 'input',}
        
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'grade', 'subject', 'classroom', 'created_date', 'due_date', 'created_by',]