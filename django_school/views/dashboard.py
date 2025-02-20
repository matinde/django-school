from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.utils import timezone
from datetime import timedelta
from ..models import (
    School, Student, Teacher, Parent, 
    Classroom, Exam, Subject, Assignment,
    Announcements, Grade
)
from ..mixins import RoleBasedAccessMixin

# create a dashboard view 
class DashboardView(RoleBasedAccessMixin, ListView):
    template_name = "home/dashboard.html"
    model = School
    context_object_name = "all_data"

    def dispatch(self, request, *args, **kwargs):
        # Check if any school exists
        if not School.objects.exists() and request.user.is_authenticated and request.user.user_type == 'admin':
            messages.info(request, "Please set up your school first before proceeding.")
            return redirect('register_school')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Basic context for all users
        context['user_type'] = user.user_type
        context['full_name'] = user.get_full_name()

        if user.user_type == 'admin':
            self._add_admin_context(context)
        elif user.user_type == 'teacher':
            self._add_teacher_context(context)
        elif user.user_type == 'parent':
            self._add_parent_context(context)
        elif user.user_type == 'student':
            self._add_student_context(context)

        return context

    def _add_admin_context(self, context):
        """Add admin-specific dashboard data"""
        context['students'] = Student.objects.all()
        context['teachers'] = Teacher.objects.all()
        context['parents'] = Parent.objects.all()
        context['classrooms'] = Classroom.objects.all()
        context['subjects'] = Subject.objects.all()

        context['student_count'] = Student.objects.count()
        context['teacher_count'] = Teacher.objects.count()
        context['parent_count'] = Parent.objects.count()
        context['class_count'] = Classroom.objects.count()
        
        context['department_stats'] = {
            'sciences': Teacher.objects.filter(department='sciences').count(),
            'arts': Teacher.objects.filter(department='arts').count(),
            'commerce': Teacher.objects.filter(department='commerce').count(),
        }
        
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        context['recent_assignments'] = Assignment.objects.filter(
            created_date__gte=thirty_days_ago
        ).order_by('-created_date')[:5]
        
        context['recent_announcements'] = Announcements.objects.all().order_by('-date')[:5]
        
        grades = Grade.objects.all()
        grade_stats = []
        for grade in grades:
            grade_stats.append({
                'name': grade.name,
                'student_count': Student.objects.filter(grade=grade).count(),
                'subject_count': grade.subjects.count()
            })
        context['grade_stats'] = grade_stats

    def _add_teacher_context(self, context):
        """Add teacher-specific dashboard data"""
        teacher = self.request.user.teacher_profile
        context['my_subjects'] = Subject.objects.filter(teacher=teacher)
        context['my_assignments'] = Assignment.objects.filter(created_by=teacher).order_by('-created_date')[:5]
        context['my_students'] = Student.objects.filter(grade__subjects__teacher=teacher).distinct()
        context['recent_announcements'] = Announcements.objects.filter(
            grade__in=Grade.objects.filter(subjects__teacher=teacher)
        ).distinct().order_by('-date')[:5]

    def _add_parent_context(self, context):
        """Add parent-specific dashboard data"""
        parent = self.request.user.parent_profile
        context['my_children'] = Student.objects.filter(parents=parent)
        # Get assignments and announcements for all children
        children_grades = Grade.objects.filter(student__in=context['my_children'])
        context['children_assignments'] = Assignment.objects.filter(
            grade__in=children_grades
        ).order_by('-created_date')[:5]
        context['recent_announcements'] = Announcements.objects.filter(
            grade__in=children_grades
        ).order_by('-date')[:5]

    def _add_student_context(self, context):
        """Add student-specific dashboard data"""
        student = self.request.user.student_profile
        context['my_grade'] = student.grade
        context['my_subjects'] = student.get_subjects()
        context['my_assignments'] = Assignment.objects.filter(
            grade=student.grade
        ).order_by('-created_date')[:5]
        context['recent_announcements'] = Announcements.objects.filter(
            grade=student.grade
        ).order_by('-date')[:5]