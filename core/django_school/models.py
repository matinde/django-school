from django.db import models
import uuid

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    logo = models.ImageField()
    website = models.CharField(max_length=255)
    phone_numbers = models.CharField(max_length=255)
    motto = models.CharField(max_length=255)
    email = models.EmailField()

class Teacher(models.Model):

    STATUS = [("active", "Active"), ("inactive", "Inactive")]
    GENDER = [("male", "Male"), ("female", "Female")]

    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_status = models.CharField(max_length=10, choices=STATUS, default="active")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_numbers = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    photo = models.ImageField()

    def __str__(self):
        return self.first_name + "" + self.last_name

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
    exam_results = models.ForeignKey(Exam, on_delete=models.CASCADE)
    
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

    def get_all_subjects(self):
        """
        A grade has many set subjects. But we expect that any given grade is set for every learner in that grade. 
        """
        return self.subjects.all()

    def add_subject(self, subject):
        """
        Administrators, can add subjects to a certain grade, in lower learning institutions.
        However, in upper learning institutions like Universities, the learner adds the subjects.
        """
        return self.subjects.add(subject)

    def remove_subject(self, subject):
        """
        Removes a subject from a grade.
        """
        return self.subjects.remove(subject)

    def edit_subject(self, name, teacher, description, grade, duration):
        """
        Edits a subject from a grade.
        """
        self.name = name
        self.teacher = teacher
        self.description = description
        self.grade = grade
        self.duration = duration
        self.save()



class Student(models.Model):
    """
    This is the main model that holds all relationships from Parents, School, Teachers, Grade
    and will also include the financial statements for each student. 
    """

    STATUS = [("active", "Active"), ("inactive", "Inactive")]

    GENDER = [("male", "Male"), ("female", "Female")]

    uid = models.UUIDField(default=uuid.uuid4, editable=False)
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
    
    
    def __str__(self):
        return self.first_name + "" + self.last_name

    def get_subjects(self):
        """
        Retrieves all the subjects for this student through the grade relationship.
        """
        return self.grade.subjects.all()


class Parent(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_numbers = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    identification_number = models.CharField(max_length=255)
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.first_name + "" + self.last_name



