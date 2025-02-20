from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from ..models import Assignment, Grade, Subject
from ..mixins import TeacherOrAdminRequiredMixin, RoleBasedAccessMixin

class AssignmentListView(RoleBasedAccessMixin, ListView):
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'teacher':
            # Teachers see assignments they created
            return Assignment.objects.filter(created_by=user.teacher_profile)
        elif user.user_type == 'student':
            # Students see assignments for their grade
            return Assignment.objects.filter(grade=user.student_profile.grade)
        elif user.user_type == 'parent':
            # Parents see assignments for their children's grades
            children = user.parent_profile.students.all()
            grades = Grade.objects.filter(student__in=children)
            return Assignment.objects.filter(grade__in=grades)
        else:
            # Admin sees all assignments
            return Assignment.objects.all()

class AssignmentDetailView(RoleBasedAccessMixin, DetailView):
    model = Assignment
    template_name = 'assignments/assignment_detail.html'
    context_object_name = 'assignment'

class AssignmentCreateView(TeacherOrAdminRequiredMixin, CreateView):
    model = Assignment
    template_name = 'assignments/assignment_form.html'
    fields = ['title', 'description', 'subject', 'grade', 'classroom', 'due_date']
    success_url = reverse_lazy('assignments')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.teacher_profile
        form.instance.created_date = timezone.now()
        messages.success(self.request, 'Assignment created successfully.')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.user_type == 'teacher':
            # Limit subject choices to teacher's subjects
            form.fields['subject'].queryset = Subject.objects.filter(teacher=self.request.user.teacher_profile)
            # Limit grade choices to grades where teacher teaches
            form.fields['grade'].queryset = Grade.objects.filter(subjects__teacher=self.request.user.teacher_profile).distinct()
        return form

class AssignmentUpdateView(TeacherOrAdminRequiredMixin, UpdateView):
    model = Assignment
    template_name = 'assignments/assignment_form.html'
    fields = ['title', 'description', 'subject', 'grade', 'classroom', 'due_date']
    success_url = reverse_lazy('assignments')

    def get_queryset(self):
        if self.request.user.user_type == 'teacher':
            return Assignment.objects.filter(created_by=self.request.user.teacher_profile)
        return Assignment.objects.all()

    def form_valid(self, form):
        messages.success(self.request, 'Assignment updated successfully.')
        return super().form_valid(form)

class AssignmentDeleteView(TeacherOrAdminRequiredMixin, DeleteView):
    model = Assignment
    template_name = 'assignments/assignment_confirm_delete.html'
    success_url = reverse_lazy('assignments')

    def get_queryset(self):
        if self.request.user.user_type == 'teacher':
            return Assignment.objects.filter(created_by=self.request.user.teacher_profile)
        return Assignment.objects.all()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Assignment deleted successfully.')
        return super().delete(request, *args, **kwargs) 