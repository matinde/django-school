# create modelforms
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import (
    Student, Teacher, Parent, Classroom, 
    Exam, Subject, Announcements, Assignment, 
    Grade, UserProfile, School
)

User = get_user_model()

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        help_text='Enter a strong password for the student account.'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        help_text='Enter the same password as above, for verification.'
    )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        # Add input class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'input'}
        
    class Meta:
        model = Student
        fields = [
            "first_name", "last_name", "email",
            "registration_number", "admission_date",
            "grade", "classroom", "date_of_birth",
            "photo", "password1", "password2"
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            try:
                # Create the user first
                user_obj = User.objects.create_user(
                    email=self.cleaned_data['email'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    user_type='student',
                    is_active=True,
                    password=self.cleaned_data['password1']  # Set the password here
                )
                
                # Set the school for the user
                school = School.objects.first()
                user_obj.school = school
                user_obj.save()
                
                # Create UserProfile for the student
                UserProfile.objects.create(
                    user=user_obj,
                    school=school
                )
                
                student.user = user_obj
                student.save()
            except Exception as e:
                raise forms.ValidationError(f"Student creation failed: {str(e)}")
        return student
            
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["status", "gender", "department", "photo"]

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'input'}

class ParentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    identification_number = forms.CharField(max_length=255)

    class Meta:
        model = Parent
        fields = ["first_name", "last_name", "email", "phone_number", "identification_number"]

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'input'}

    def save(self, commit=True):
        try:
            parent = super().save(commit=False)
            if commit:
                # Create the user first
                user_obj = User.objects.create_user(
                    email=self.cleaned_data['email'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    user_type='parent',
                    is_active=True
                )
                parent.user = user_obj
                parent.identification_number = self.cleaned_data['identification_number']
                parent.save()
                
                # Create UserProfile
                school = School.objects.first()
                UserProfile.objects.create(
                    user=user_obj,
                    phone_number=self.cleaned_data['phone_number'],
                    school=school
                )
            return parent
        except Exception as e:
            raise forms.ValidationError(f"Parent creation failed: {str(e)}")

class ClassroomForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClassroomForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs = {'class': 'input',}
        
    class Meta:
        model = Classroom
        fields = ['name',]

class GradeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs = {'class': 'input',}
        self.fields['subjects'].widget.attrs = {'class': 'input',}

    class Meta:
        model = Grade
        fields = ['name', 'subjects',]

class ExamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs = {'class': 'input',}
        self.fields['year'].widget.attrs = {'class': 'input',}
        self.fields['month'].widget.attrs = {'class': 'input',}
        self.fields['day'].widget.attrs = {'class': 'input',}
        self.fields['term'].widget.attrs = {'class': 'input',}
     
    class Meta:
        model = Exam
        fields = ['name', 'year', 'month', 'day', 'term',]

class SubjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs = {'class': 'input',}
        self.fields['teacher'].widget.attrs = {'class': 'input',}
        self.fields['description'].widget.attrs = {'class': 'input',}
        self.fields['duration'].widget.attrs = {'class': 'input',}
        self.fields['exam_results'].widget.attrs = {'class': 'input',}
      
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'description', 'duration', 'exam_results',]

class AnnouncementsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnnouncementsForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs = {'class': 'input',}
        self.fields['description'].widget.attrs = {'class': 'input',}
        self.fields['grade'].widget.attrs = {'class': 'input',}
        self.fields['date'].widget.attrs = {'class': 'input',}
        
    class Meta:
        model = Announcements
        fields = ['title', 'description', 'grade', 'date',]

class AssignmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs = {'class': 'input',}
        self.fields['description'].widget.attrs = {'class': 'input',}
        self.fields['grade'].widget.attrs = {'class': 'input',}
        self.fields['subject'].widget.attrs = {'class': 'input',}
        self.fields['classroom'].widget.attrs = {'class': 'input',}
        self.fields['created_date'].widget.attrs = {'class': 'input',}
        self.fields['due_date'].widget.attrs = {'class': 'input',}
        self.fields['created_by'].widget.attrs = {'class': 'input',}
        
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'grade', 'subject', 'classroom', 'created_date', 'due_date', 'created_by',]

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = self.authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Your email or password is incorrect. Please try again.",
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

class BaseUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})

class AdminRegistrationForm(BaseUserRegistrationForm):
    class Meta(BaseUserRegistrationForm.Meta):
        fields = BaseUserRegistrationForm.Meta.fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'admin'
        user.is_approved = True
        user.approval_status = 'approved'
        if commit:
            user.save()
        return user

class TeacherRegistrationForm(BaseUserRegistrationForm):
    phone_number = forms.CharField(max_length=20)
    gender = forms.ChoiceField(choices=Teacher.GENDER)
    department = forms.ChoiceField(choices=Teacher.DEPARTMENT)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    photo = forms.ImageField(required=False)

    class Meta(BaseUserRegistrationForm.Meta):
        fields = BaseUserRegistrationForm.Meta.fields + ('phone_number', 'gender', 'department', 'bio', 'photo')

    def clean(self):
        cleaned_data = super().clean()
        if 'password1' in cleaned_data and 'password2' in cleaned_data:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data

    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.user_type = 'teacher'
            user.is_active = True
            
            # Explicitly set the password
            if self.cleaned_data.get('password1'):
                user.set_password(self.cleaned_data['password1'])
            
            if commit:
                user.save()
                school = School.objects.first()
                user.school = school
                user.save()
                
                Teacher.objects.create(
                    user=user,
                    gender=self.cleaned_data['gender'],
                    department=self.cleaned_data['department'],
                    photo=self.cleaned_data.get('photo'),
                    status='active'
                )
                
                UserProfile.objects.create(
                    user=user,
                    phone_number=self.cleaned_data['phone_number'],
                    bio=self.cleaned_data.get('bio', ''),
                    school=school
                )
            return user
        except Exception as e:
            raise forms.ValidationError(f"Registration failed: {str(e)}")

class ParentRegistrationForm(BaseUserRegistrationForm):
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    identification_number = forms.CharField(max_length=255)
    
    class Meta(BaseUserRegistrationForm.Meta):
        fields = BaseUserRegistrationForm.Meta.fields + ('phone_number', 'address', 'identification_number')

    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.user_type = 'parent'
            user.is_active = True  # Parents are auto-approved
            
            if commit:
                user.save()
                school = School.objects.first()
                user.school = school
                user.save()
                
                # Create Parent profile
                Parent.objects.create(
                    user=user,
                    identification_number=self.cleaned_data['identification_number']
                )
                
                # Create UserProfile
                UserProfile.objects.create(
                    user=user,
                    phone_number=self.cleaned_data['phone_number'],
                    address=self.cleaned_data['address'],
                    school=school
                )
            return user
        except Exception as e:
            raise forms.ValidationError(f"Registration failed: {str(e)}")

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        if commit:
            user.save()
        return user

class SchoolRegistrationForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('created_by', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})
        self.fields['motto'].widget.attrs.update({'class': 'textarea'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})
        self.fields['bio'].widget.attrs.update({'class': 'textarea'})
        self.fields['address'].widget.attrs.update({'class': 'textarea'})