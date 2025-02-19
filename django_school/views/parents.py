from django.shortcuts import render, get_object_or_404, reverse
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
    template_name = "parents/parents.html"
    model = Parent
    context_object_name = "parents"
    paginate_by = 10

# Create a view for one subject

class ParentDetailView(DetailView):
    template_name = "parents/parent_detail.html"
    model = Parent
    context_object_name = "parent"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Parent, uid=pk)

    # Get the list of students for this parent
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = self.object.students.all()
        return context

class ParentCreateView(CreateView):
    template_name = "parents/parent_form.html"
    model = Parent
    form_class = ParentForm
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Parent created successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error creating parent.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("parent_detail", kwargs={"pk": self.object.uid})

class ParentUpdateView(UpdateView):
    template_name = "parents/parent_form.html"
    model = Parent
    form_class = ParentForm

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Parent, uid=pk)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Parent updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error updating parent.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("parent_detail", kwargs={"pk": self.object.uid})

class ParentDeleteView(DeleteView):
    template_name = "parents/subject_delete.html"
    model = Subject
    context_object_name = "parent"
    success_url = "/parents/"
    
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Parent, pk=pk)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Subject deleted successfully.")
        return super().delete(request, *args, **kwargs)
