from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django_school.forms import StudentForm, TeacherForm, ParentForm, ClassroomForm, ExamForm, SubjectForm
from django_school.models import (
    School, Student, Teacher, Parent, Classroom, 
    Exam, Subject, Grade
)
from ..mixins import TeacherOrAdminRequiredMixin, ParentOrAdminRequiredMixin

User = get_user_model()

# Create a dashboard view that will display the number of students, teachers, parents, schools, classrooms, exams and subjects
# in the school system. The dashboard view should be displayed on the home page of the application.


class StudentListView(TeacherOrAdminRequiredMixin, ListView):
    template_name = "students/students.html"
    model = Student
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.user_type == 'teacher':
            # Teachers can only see students in their classes
            teacher = self.request.user.teacher_profile
            return queryset.filter(grade__subjects__teacher=teacher).distinct()
        return queryset

class StudentDetailView(TeacherOrAdminRequiredMixin, DetailView):
    template_name = "students/student_detail.html"
    model = Student
    context_object_name = "student"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.user_type == 'teacher':
            # Verify the student is in teacher's class
            if not obj.grade.subjects.filter(teacher__email=self.request.user.email).exists():
                messages.error(self.request, "You do not have permission to view this student's details.")
                return redirect('students')
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parents'] = self.object.parents.all()
        context['subjects'] = self.object.grade.subjects.all()
        return context

class StudentCreateView(ParentOrAdminRequiredMixin, CreateView):
    template_name = "students/student_form.html"
    model = Student
    form_class = StudentForm
    
    def form_valid(self, form):
        try:
            student = form.save(commit=False)
            
            # Create user for the student
            user_obj = User.objects.create_user(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                user_type='student',
                is_active=True,
                school=self.request.user.school
            )
            student.user = user_obj
            student.save()
            
            # If parent is creating, automatically associate the student with them
            if self.request.user.user_type == 'parent':
                student.parents.add(self.request.user.parent_profile)
                messages.success(self.request, "Student registered successfully and added to your children.")
            else:
                messages.success(self.request, "Student created successfully.")
            
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error creating student: {str(e)}")
            return self.form_invalid(form)

    def get_success_url(self):
        if self.request.user.user_type == 'parent':
            return reverse('children')  # Redirect to children list for parents
        return reverse("student_detail", kwargs={"pk": self.object.pk})

class StudentUpdateView(ParentOrAdminRequiredMixin, UpdateView):
    template_name = "students/student_form.html"
    model = Student
    form_class = StudentForm

    def get_object(self):
        obj = super().get_object()
        if self.request.user.user_type == 'parent':
            # Verify the student belongs to this parent
            if not obj.parents.filter(user=self.request.user).exists():
                messages.error(self.request, "You do not have permission to edit this student's details.")
                return redirect('students')
        return obj
    
    def get_initial(self):
        # Pre-populate form with user data
        initial = super().get_initial()
        if self.object:
            initial['first_name'] = self.object.user.first_name
            initial['last_name'] = self.object.user.last_name
            initial['email'] = self.object.user.email
        return initial
    
    def form_valid(self, form):
        try:
            student = form.save(commit=False)
            # Update the associated user
            student.user.first_name = form.cleaned_data['first_name']
            student.user.last_name = form.cleaned_data['last_name']
            student.user.email = form.cleaned_data['email']
            student.user.save()
            student.save()
            messages.success(self.request, "Student updated successfully.")
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Error updating student: {str(e)}")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("student_detail", kwargs={"pk": self.object.pk})

class StudentDeleteView(ParentOrAdminRequiredMixin, DeleteView):
    template_name = "students/student_confirm_delete.html"
    model = Student
    
    def get_object(self):
        obj = super().get_object()
        if self.request.user.user_type == 'parent':
            # Verify the student belongs to this parent
            if not obj.parents.filter(email=self.request.user.email).exists():
                messages.error(self.request, "You do not have permission to delete this student.")
                return redirect('students')
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Student deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("students")



