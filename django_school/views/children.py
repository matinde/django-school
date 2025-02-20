from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from ..models import Student
from ..mixins import ParentRequiredMixin

class ChildrenListView(ParentRequiredMixin, ListView):
    template_name = 'children/children_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        # Get all students associated with the logged-in parent through the M2M relationship
        return Student.objects.filter(parents=self.request.user.parent_profile).select_related(
            'user', 'grade', 'classroom'
        ).order_by('user__first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context if needed
        return context

class ChildDetailView(ParentRequiredMixin, DetailView):
    model = Student
    template_name = 'children/child_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        # Only allow parents to view their own children's details
        return Student.objects.filter(
            parents=self.request.user.parent_profile
        ).select_related('user', 'grade', 'classroom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        context.update({
            'subjects': student.grade.subjects.all().select_related('teacher'),
            'assignments': student.grade.assignment_set.all().order_by('-created_date')[:5],
            'announcements': student.grade.announcements_set.all().order_by('-date')[:5]
        })
        return context 