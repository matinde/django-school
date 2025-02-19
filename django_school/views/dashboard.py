from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_school.forms import StudentForm, TeacherForm, ParentForm, ClassroomForm, ExamForm, SubjectForm
from django_school.models import School
from django_school.models import Student
from django_school.models import Teacher
from django_school.models import Parent
from django_school.models import Classroom
from django_school.models import Exam
from django_school.models import Subject

# create a dashboard view 
class DashboardView(ListView):
    template_name = "home/dashboard.html"
    model = School
    context_object_name = "all_data"

    def get_context_data(self, **kwargs):
        """
        Adding all models to the dashboard will help administrators to search and get data.
        We can optimize it later.
        """
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        context['teachers'] = Teacher.objects.all()
        context['parents'] = Parent.objects.all()
        context['classrooms'] = Classroom.objects.all()
        context['subjects'] = Subject.objects.all()

        context['student_number'] = Student.objects.all().count()
        context['teacher_number'] = Teacher.objects.all().count()
        context['parent_number'] = Parent.objects.all().count()
        context['classroom_number'] = Classroom.objects.all().count()
        context['exam_number'] = Exam.objects.all().count()
        context['subject_number'] = Subject.objects.all().count()

        return context