from django.urls import path
from django_school.views import dashboard

from django_school.views.students import *
from django_school.views.subjects import *
from django_school.views.teachers import *
from django_school.views.parents import *
from django_school.views.dashboard import *

urlpatterns = [

    # Home
    path("", DashboardView.as_view(), name="home"),
   

    # Students
    path("students/", StudentListView.as_view(), name="students"),
    path("student/create/", StudentCreateView.as_view(), name="student_create"),
    path("student/<int:uid>/", StudentDetailView.as_view(), name="student_detail"),
    path("student/<int:uid>/update/", StudentUpdateView.as_view(), name="student_update"),
    path("student/<int:uid>/delete/", StudentDeleteView.as_view(), name="student_delete"),

    # Subjects
    path("subjects/", SubjectListView.as_view(), name="subjects"),
    path("subject/create/", SubjectCreateView.as_view(), name="subject_create"),
    path("subject/<int:uid>/", SubjectDetailView.as_view(), name="subject_detail"),
    path("subject/<int:uid>/update/", SubjectUpdateView.as_view(), name="subject_update"),
    path("subject/<int:uid>/delete/", SubjectDeleteView.as_view(), name="subject_delete"),

    # Teachers
    path("teachers/", TeacherListView.as_view(), name="teachers"),
    path("teacher/create/", TeacherCreateView.as_view(), name="teacher_create"),
    path("teacher/<int:uid>/", TeacherDetailView.as_view(), name="teacher_detail"),
    path("teacher/<int:uid>/update/", TeacherUpdateView.as_view(), name="teacher_update"),
    path("teacher/<int:uid>/delete/", TeacherDeleteView.as_view(), name="teacher_delete"),

    # Parents
    path("parents/", ParentListView.as_view(), name="parents"),
    path("parent/create/", ParentCreateView.as_view(), name="parent_create"),
    path("parent/<int:uid>/", ParentDetailView.as_view(), name="parent_detail"),
    path("parent/<int:uid>/update/", ParentUpdateView.as_view(), name="parent_update"),
    path("parent/<int:uid>/delete/", ParentDeleteView.as_view(), name="parent_delete"),

]
