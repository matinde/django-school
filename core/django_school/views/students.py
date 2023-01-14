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

# Create a dashboard view that will display the number of students, teachers, parents, schools, classrooms, exams and subjects
# in the school system. The dashboard view should be displayed on the home page of the application.


class StudentListView(ListView):
    template_name = "students/students.html"
    model = Student
    context_object_name = "students"
    paginate_by = 10 

class StudentDetailView(DetailView):
    template_name = "students/student_detail.html"
    model = Student
    context_object_name = "student"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Student, uid=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parents'] = self.object.parents.all()
        context['subjects'] = self.object.grade.subjects.all()
        return context

class StudentCreateView(CreateView):
    template_name = "students/student_form.html"
    model = Student
    form_class = StudentForm
    
    def form_valid(self, form): 
        form.save()
        messages.success(self.request, "Student created successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error creating student.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("student_detail", kwargs={"pk": self.object.uid})

class StudentUpdateView(UpdateView):
    template_name = "students/student_form.html"
    model = Student
    form_class = StudentForm
    context_object_name = "student"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Student, uid=pk)
    
    def form_valid(self, form):
        form.save() 
        messages.success(self.request, "Student updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error updating student.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("student_detail", kwargs={"pk": self.object.uid})

class StudentDeleteView(DeleteView):
    template_name = "students/student_delete.html"
    model = Student
    context_object_name = "student"
    success_url = "/students/"
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Student deleted successfully.")
        return super().delete(request, *args, **kwargs)



