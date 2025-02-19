from django.shortcuts import render, get_object_or_404, reverse, redirect
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

class SubjectListView(ListView):
    template_name = "subjects/subjects.html"
    model = Subject
    context_object_name = "subjects"
    paginate_by = 10

# Create a view for one subject

class SubjectDetailView(DetailView):
    template_name = "subjects/subject_detail.html"
    model = Subject
    context_object_name = "subject"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Subject, uid=pk)

class SubjectCreateView(CreateView):
    template_name = "subjects/subject_form.html"
    model = Subject
    form_class = SubjectForm
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Subject created successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error creating subject.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("subject_detail", kwargs={"pk": self.object.uid})

class SubjectUpdateView(UpdateView):
    template_name = "subjects/subject_form.html"
    model = Subject
    form_class = SubjectForm

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Subject, uid=pk)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Subject updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error updating subject.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("subject_detail", kwargs={"pk": self.object.uid})

class SubjectDeleteView(DeleteView):
    template_name = "subject_delete.html"
    model = Subject
    context_object_name = "subject"
    success_url = "/subjects/"
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Subject deleted successfully.")
        return super().delete(request, *args, **kwargs)