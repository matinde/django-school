from django.db import models
import uuid
from django.contrib.auth.models import User
from .utils import get_upload_path

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    logo = models.ImageField()
    website = models.CharField(max_length=255)
    phone_numbers = models.CharField(max_length=255)
    motto = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Teacher(models.Model):

    STATUS = [("active", "Active"), ("inactive", "Inactive")]
    GENDER = [("male", "Male"), ("female", "Female")]
    DEPARTMENT = [("sciences", "Sciences"), ("arts", "Arts"), ("commerce", "Commerce")]

    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_status = models.CharField(max_length=10, choices=STATUS, default="active")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_numbers = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    department = models.CharField(max_length=255, choices=DEPARTMENT, blank=True, null=True)
    photo = models.ImageField()

    def __str__(self):
        return self.first_name + " " + self.last_name

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
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_numbers = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    identification_number = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Student(models.Model):
    """
    This is the main model that holds all relationships from Parents, School, Teachers, Grade
    and will also include the financial statements for each student. 
    """

    STATUS = [("active", "Active"), ("inactive", "Inactive")]
    GENDER = [("male", "Male"), ("female", "Female")]

    uid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    current_status = models.CharField(max_length=10, choices=STATUS, default="active")
    registration_number = models.IntegerField()
    admission_date = models.DateField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    parents = models.ManyToManyField(Parent, related_name='students', blank=True)
    
    
    def __str__(self):
        return self.first_name + " " + self.last_name

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
