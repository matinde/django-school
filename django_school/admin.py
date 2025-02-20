from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    user, School, Teacher, Parent, Student,
    Grade, Subject, Classroom, Assignment,
    Announcements, UserProfile
)
from django.utils import timezone

@admin.register(user)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('School', {'fields': ('school',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_active', 'school'),
        }),
    )

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'email', 'department', 'status')
    list_filter = ('status', 'department')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    list_editable = ('status',)  # Allow quick status changes right from the list view
    
    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Name'
    
    def email(self, obj):
        return obj.user.email
    
    fieldsets = (
        ('Teacher Information', {
            'fields': ('user', 'status', 'department', 'gender', 'photo')
        }),
    )

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_email', 'identification_number')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'identification_number')
    
    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_email', 'registration_number', 'grade', 'classroom')
    list_filter = ('grade', 'classroom')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'registration_number')
    
    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website')
    search_fields = ('name', 'email')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('subjects',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'duration')
    list_filter = ('teacher',)
    search_fields = ('name',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade', 'created_date', 'due_date')
    list_filter = ('grade', 'subject')
    search_fields = ('title',)

@admin.register(Announcements)
class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'date')
    list_filter = ('grade',)
    search_fields = ('title',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__email', 'phone_number')