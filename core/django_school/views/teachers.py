from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_school.forms import StudentForm, TeacherForm, ParentForm, ClassroomForm, ExamForm, SubjectForm
from django_school.models import Student
from django_school.models import Teacher
from django_school.models import Parent
from django_school.models import Classroom
from django_school.models import Exam
from django_school.models import Subject


class TeacherListView(ListView):
    template_name = "teachers.html"
    model = Teacher
    context_object_name = "teachers"
    paginate_by = 10

# Create a view for one teacher

class TeacherDetailView(DetailView):
    template_name = "teacher_detail.html"
    model = Teacher
    context_object_name = "teacher"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Teacher, pk=pk)

class TeacherCreateView(CreateView):
    template_name = "student_form.html"
    model = Teacher
    form_class = TeacherForm
    success_url = "/teachers/"
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Teacher created successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error creating teacher.")
        return super().form_invalid(form)

class TeacherUpdateView(UpdateView):
    template_name = "teacher_form.html"
    model = Teacher
    form_class = TeacherForm
    success_url = "/teachers/"
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Teacher updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error updating teacher.")
        return super().form_invalid(form)

class TeacherDeleteView(DeleteView):
    template_name = "teacher_delete.html"
    model = Teacher
    context_object_name = "teacher"
    success_url = "/teachers/"
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Teacher deleted successfully.")
        return super().delete(request, *args, **kwargs)