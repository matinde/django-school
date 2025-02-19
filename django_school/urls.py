from django.urls import path
from django_school.views import dashboard

from django_school.views.students import *
from django_school.views.subjects import *
from django_school.views.teachers import *
from django_school.views.parents import *
from django_school.views.dashboard import *
from django_school.views.grades import *

urlpatterns = [

    # Home
    path("", DashboardView.as_view(), name="home"),
   

    # Students
    path("students/", StudentListView.as_view(), name="students"),
    path("student/create/", StudentCreateView.as_view(), name="student_create"),
    path("student/<str:pk>/", StudentDetailView.as_view(), name="student_detail"),
    path("student/<str:pk>/update/", StudentUpdateView.as_view(), name="student_update"),
    path("student/<int:pk>/delete/", StudentDeleteView.as_view(), name="student_delete"),

    # Subjects
    path("subjects/", SubjectListView.as_view(), name="subjects"),
    path("subject/create/", SubjectCreateView.as_view(), name="subject_create"),
    path("subject/<str:pk>/", SubjectDetailView.as_view(), name="subject_detail"),
    path("subject/<str:pk>/update/", SubjectUpdateView.as_view(), name="subject_update"),
    path("subject/<str:pk>/delete/", SubjectDeleteView.as_view(), name="subject_delete"),

    # Teachers
    path("teachers/", TeacherListView.as_view(), name="teachers"),
    path("teacher/create/", TeacherCreateView.as_view(), name="teacher_create"),
    path("teacher/<str:pk>/", TeacherDetailView.as_view(), name="teacher_detail"),
    path("teacher/<str:pk>/update/", TeacherUpdateView.as_view(), name="teacher_update"),
    path("teacher/<str:pk>/delete/", TeacherDeleteView.as_view(), name="teacher_delete"),

    # Parents
    path("parents/", ParentListView.as_view(), name="parents"),
    path("parent/create/", ParentCreateView.as_view(), name="parent_create"),
    path("parent/<str:pk>/", ParentDetailView.as_view(), name="parent_detail"),
    path("parent/<str:pk>/update/", ParentUpdateView.as_view(), name="parent_update"),
    path("parent/<str:pk>/delete/", ParentDeleteView.as_view(), name="parent_delete"),

    # Grades
    path("grades/", GradeListView.as_view(), name="grades"),
    path("grade/create/", GradeCreateView.as_view(), name="grade_create"),
    path("grade/<str:pk>/", GradeDetailView.as_view(), name="grade_detail"),
    path("grade/<str:pk>/update/", GradeUpdateView.as_view(), name="grade_update"),
    path("grade/<str:pk>/delete/", GradeDeleteView.as_view(), name="grade_delete"),

]
