from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_school.forms import StudentForm, TeacherForm, ParentForm, ClassroomForm, ExamForm, SubjectForm
from django_school.models import Student
from django_school.models import Teacher
from django_school.models import Parent
from django_school.models import Classroom
from django_school.models import Exam
from django_school.models import Subject
from ..mixins import AdminRequiredMixin, TeacherOrAdminRequiredMixin


class TeacherListView(TeacherOrAdminRequiredMixin, ListView):
    template_name = "teachers/teachers.html"
    model = Teacher
    context_object_name = "teachers"
    paginate_by = 10

# Create a view for one teacher

class TeacherDetailView(TeacherOrAdminRequiredMixin, DetailView):
    template_name = "teachers/teacher_detail.html"
    model = Teacher
    context_object_name = "teacher"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.user_type == 'teacher' and obj.email != self.request.user.email:
            messages.error(self.request, "You can only view your own profile.")
            return redirect('teachers')
        return obj

class TeacherCreateView(AdminRequiredMixin, CreateView):
    template_name = "teachers/teacher_form.html"
    model = Teacher
    form_class = TeacherForm
    
    def form_valid(self, form):
        try:
            teacher = form.save()
            messages.success(self.request, "Teacher created successfully.")
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error creating teacher: {str(e)}")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("teacher_detail", kwargs={"pk": self.object.pk})

class TeacherUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "teachers/teacher_form.html"
    model = Teacher
    form_class = TeacherForm

    def get_initial(self):
        # Pre-populate form with user data
        initial = super().get_initial()
        if self.object:
            initial['first_name'] = self.object.user.first_name
            initial['last_name'] = self.object.user.last_name
            initial['email'] = self.object.user.email
            if hasattr(self.object.user, 'profile'):
                initial['phone_number'] = self.object.user.profile.phone_number
        return initial
    
    def form_valid(self, form):
        try:
            teacher = form.save(commit=False)
            # Update the associated user
            teacher.user.first_name = form.cleaned_data['first_name']
            teacher.user.last_name = form.cleaned_data['last_name']
            teacher.user.email = form.cleaned_data['email']
            teacher.user.save()
            
            # Update profile
            if hasattr(teacher.user, 'profile'):
                teacher.user.profile.phone_number = form.cleaned_data.get('phone_number')
                teacher.user.profile.save()
            
            teacher.save()
            messages.success(self.request, "Teacher updated successfully.")
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error updating teacher: {str(e)}")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("teacher_detail", kwargs={"pk": self.object.pk})

class TeacherDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "teachers/teacher_confirm_delete.html"
    model = Teacher
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Teacher deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("teachers")