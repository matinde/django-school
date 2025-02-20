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
        try:
            parent = form.save()
            messages.success(self.request, "Parent created successfully.")
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error creating parent: {str(e)}")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("parent_detail", kwargs={"pk": self.object.pk})

class ParentUpdateView(UpdateView):
    template_name = "parents/parent_form.html"
    model = Parent
    form_class = ParentForm

    def get_initial(self):
        # Pre-populate form with user data
        initial = super().get_initial()
        if self.object:
            initial['first_name'] = self.object.user.first_name
            initial['last_name'] = self.object.user.last_name
            initial['email'] = self.object.user.email
            initial['phone_number'] = self.object.user.profile.phone_number
        return initial
    
    def form_valid(self, form):
        try:
            parent = form.save(commit=False)
            # Update the associated user
            parent.user.first_name = form.cleaned_data['first_name']
            parent.user.last_name = form.cleaned_data['last_name']
            parent.user.email = form.cleaned_data['email']
            parent.user.save()
            
            # Update profile
            parent.user.profile.phone_number = form.cleaned_data['phone_number']
            parent.user.profile.save()
            
            parent.save()
            messages.success(self.request, "Parent updated successfully.")
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error updating parent: {str(e)}")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("parent_detail", kwargs={"pk": self.object.pk})

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
