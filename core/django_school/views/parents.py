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

class ParentListView(ListView):
    template_name = "parents.html"
    model = Parent
    context_object_name = "parents"
    paginate_by = 10

# Create a view for one subject

class ParentDetailView(DetailView):
    template_name = "parent_detail.html"
    model = Parent
    context_object_name = "parent"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Subject, uid=pk)

class ParentCreateView(CreateView):
    template_name = "subject_form.html"
    model = Parent
    form_class = ParentForm
    success_url = "/parents/"
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Parent created successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error creating parent.")
        return super().form_invalid(form)

class ParentUpdateView(UpdateView):
    template_name = "parent_form.html"
    model = Parent
    form_class = ParentForm
    success_url = "/parents/"
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Parent updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error updating parent.")
        return super().form_invalid(form)

class ParentDeleteView(DeleteView):
    template_name = "subject_delete.html"
    model = Subject
    context_object_name = "parent"
    success_url = "/parents/"
    
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Parent, pk=pk)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Subject deleted successfully.")
        return super().delete(request, *args, **kwargs)
