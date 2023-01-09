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
    context_object_name = "schools"
    paginate_by = 10
