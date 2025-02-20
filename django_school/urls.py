from django.urls import path
from django.contrib.auth import views as django_auth_views
from .views import auth as custom_auth_views
from .forms import CustomAuthenticationForm

from django_school.views import dashboard

from django_school.views.students import *
from django_school.views.subjects import *
from django_school.views.teachers import *
from django_school.views.parents import *
from django_school.views.dashboard import *
from django_school.views.grades import *
from django_school.views.assignments import *
from django_school.views.messages import *
from django_school.views.profile import *
from django_school.views.children import ChildrenListView, ChildDetailView

urlpatterns = [
    # Authentication URLs
    path('login/', custom_auth_views.CustomLoginView.as_view(), name='login'),
    path('logout/', django_auth_views.LogoutView.as_view(), name='logout'),
    path('pending-approval/', custom_auth_views.pending_approval, name='pending_approval'),
    
    # Registration URLs
    path('register/<str:user_type>/', custom_auth_views.RegisterView.as_view(), name='register'),
    path('register/student/', custom_auth_views.StudentRegisterView.as_view(), name='register_student'),
    path('register/school/', custom_auth_views.SchoolRegistrationView.as_view(), name='register_school'),
    
    # Password Reset URLs
    path('password_reset/', django_auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', django_auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', django_auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

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

    # Assignments
    path("assignments/", AssignmentListView.as_view(), name="assignments"),
    path("assignment/create/", AssignmentCreateView.as_view(), name="assignment_create"),
    path("assignment/<str:pk>/", AssignmentDetailView.as_view(), name="assignment_detail"),
    path("assignment/<str:pk>/update/", AssignmentUpdateView.as_view(), name="assignment_update"),
    path("assignment/<str:pk>/delete/", AssignmentDeleteView.as_view(), name="assignment_delete"),

    # Messages
    path("messages/", MessageListView.as_view(), name="messages"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<str:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/<str:pk>/reply/", MessageReplyView.as_view(), name="message_reply"),

    # Profile and Settings
    path("profile/", ProfileView.as_view(), name="profile"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("help/", HelpView.as_view(), name="help"),

    # Children (for parents)
    path("children/", ChildrenListView.as_view(), name="children"),
    path("child/<str:pk>/", ChildDetailView.as_view(), name="child_detail"),

    path('teachers/pending/', custom_auth_views.TeacherListView.as_view(), name='pending_teachers'),
]
