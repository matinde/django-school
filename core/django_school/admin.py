from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'logo', 'website', 'phone_numbers', 'email',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'grade', 'registration_number', 'uid', )
    list_filter = ('first_name', 'last_name', 'grade', 'registration_number', )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'current_status', 'last_name', 'email', 'phone_numbers', )
    list_filter = ('current_status', 'first_name', 'last_name', 'email', 'phone_numbers', )

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_numbers', 'identification_number', )
    list_filter = ('first_name', 'last_name', 'email', 'phone_numbers', 'identification_number', )

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'duration', )
    list_filter = ('name', 'teacher',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name',)