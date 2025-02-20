from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
from .utils import get_upload_path
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_approved', True)
        return self.create_user(email, password, **extra_fields)

class user(AbstractUser):
    USER_TYPES = [
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student')
    ]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

    @property
    def is_teacher(self):
        return self.user_type == 'teacher'

    @property
    def is_parent(self):
        return self.user_type == 'parent'

    @property
    def is_student(self):
        return self.user_type == 'student'

    @property
    def is_admin(self):
        return self.user_type == 'admin'

    class Meta:
        permissions = [
            ("can_approve_users", "Can approve user registrations"),
            ("can_view_dashboard", "Can view admin dashboard"),
            ("can_manage_school", "Can manage school settings"),
        ]

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='school_logos/')
    website = models.CharField(max_length=255)
    phone_numbers = models.CharField(max_length=255)
    motto = models.CharField(max_length=255)
    email = models.EmailField()
    created_by = models.ForeignKey('django_school.user', on_delete=models.SET_NULL, null=True, related_name='schools_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    STATUS = [("active", "Active"), ("inactive", "Inactive")]
    GENDER = [("male", "Male"), ("female", "Female")]
    DEPARTMENT = [("sciences", "Sciences"), ("arts", "Arts"), ("commerce", "Commerce")]

    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='teacher_profile')
    status = models.CharField(max_length=10, choices=STATUS, default="inactive", help_text="Set to Active to approve the teacher")
    gender = models.CharField(max_length=10, choices=GENDER)
    department = models.CharField(max_length=255, choices=DEPARTMENT, blank=True, null=True)
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"

    def save(self, *args, **kwargs):
        # When teacher status changes, update user's active status
        if self.status == 'active':
            self.user.is_active = True
            self.user.save()
        super().save(*args, **kwargs)

class Classroom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Exam(models.Model):
    
    TERMS = [("first", "First"), ("second", "Second"), ("third", "Third")]

    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    year = models.DateField()
    month = models.DateField()
    day = models.DateField()
    term = models.CharField(max_length=255, choices=TERMS)
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.TextField()
    duration = models.SmallIntegerField(help_text='This is for how long the subject takes')
    exam_results = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.name


class Grade(models.Model):
    """
    This is a class level model for each student. It also holds all the subjects that are set for that grade.
    Administrators can add subjects to a certain grade, or remove them.
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name

    


class Parent(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='parent_profile')
    identification_number = models.CharField(max_length=255)

    def __str__(self):
        return self.user.get_full_name()

class Student(models.Model):
    """
    This is the main model that holds all relationships from Parents, School, Teachers, Grade
    and will also include the financial statements for each student. 
    """

    GENDER = [("male", "Male"), ("female", "Female")]

    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.IntegerField()
    admission_date = models.DateField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    parents = models.ManyToManyField(Parent, related_name='students', blank=True)
    
    def __str__(self):
        return self.user.get_full_name()

    def get_subjects(self):
        """
        Retrieves all the subjects for this student through the grade relationship.
        """
        return self.grade.subjects.all()



class Announcements(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.title


class Assignment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created_date = models.DateField()
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    due_date = models.DateField()

    def __str__(self):
        return self.title

class Document(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_upload_path)
    user = models.ForeignKey('django_school.user', on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name() or self.user.username}"

    class Meta:
        ordering = ['-uploaded_at']

    @property
    def file_url(self):
        return self.file.url if self.file else None

class UserProfile(models.Model):
    user = models.OneToOneField('django_school.user', on_delete=models.CASCADE, related_name='profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

class Message(models.Model):
    sender = models.ForeignKey(user, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(user, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - From: {self.sender.get_full_name()} To: {self.recipient.get_full_name()}"
