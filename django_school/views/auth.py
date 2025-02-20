from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model

from ..forms import (
    CustomAuthenticationForm, AdminRegistrationForm,
    TeacherRegistrationForm, ParentRegistrationForm,
    StudentRegistrationForm, SchoolRegistrationForm
)
from ..models import user, School, Teacher, Parent, UserProfile

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Check if school exists before allowing any registration
        if not School.objects.exists():
            messages.error(request, 'School setup is required before registration. Please contact the administrator.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        user_type = self.kwargs.get('user_type')
        if user_type == 'admin':
            return AdminRegistrationForm
        elif user_type == 'teacher':
            return TeacherRegistrationForm
        elif user_type == 'parent':
            return ParentRegistrationForm
        return None

    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            # Ensure we have a school
            school = School.objects.first()
            if not school:
                raise ValueError("No school exists in the system")
            
            user.school = school
            user.save()
            
            # Create parent profile if this is a parent registration
            if user.user_type == 'parent':
                Parent.objects.create(
                    user=user,
                    identification_number=form.cleaned_data.get('identification_number')
                )
                UserProfile.objects.create(
                    user=user,
                    phone_number=form.cleaned_data.get('phone_number'),
                    address=form.cleaned_data.get('address'),
                    school=school
                )
                messages.success(self.request, 'Registration successful! You can now log in and start managing your children\'s education.')
            elif user.user_type == 'teacher':
                messages.success(
                    self.request,
                    'Registration successful! You can now log in, but some features will be restricted until an administrator approves your account.'
                )
            else:
                messages.success(self.request, 'Registration successful! You can now log in.')
            
            return redirect('login')
        except Exception as e:
            messages.error(self.request, f"Registration failed: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class StudentRegisterView(CreateView):
    form_class = StudentRegistrationForm
    template_name = 'registration/register_student.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type in ['admin', 'parent']:
            messages.error(request, 'You do not have permission to register students.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        student = form.save(commit=False)
        student.save()
        messages.success(self.request, 'Student registered successfully!')
        return redirect(self.success_url)

@method_decorator(login_required, name='dispatch')
class TeacherListView(ListView):
    template_name = 'registration/teacher_list.html'
    context_object_name = 'pending_teachers'

    def get_queryset(self):
        return Teacher.objects.filter(status='inactive')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type == 'admin':
            messages.error(request, 'You do not have permission to view pending teachers.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        # Get the ModelBackend
        from django.contrib.auth import get_backends
        backend = get_backends()[0]
        
        try:
            # Try to get the user first
            user = get_user_model().objects.get(email=email)
            
            # Verify password
            if not user.check_password(password):
                messages.error(self.request, 'Invalid email or password.')
                return self.form_invalid(form)
            
            # Check if user is active
            if not user.is_active:
                messages.error(self.request, 'Your account is not active.')
                return self.form_invalid(form)
            
            # Check teacher status if applicable
            if user.user_type == 'teacher':
                try:
                    teacher = user.teacher_profile
                    if teacher.status == 'inactive':
                        messages.error(self.request, 'Your teacher account is pending approval.')
                        return self.form_invalid(form)
                except Teacher.DoesNotExist:
                    messages.error(self.request, 'Teacher profile not found.')
                    return self.form_invalid(form)
            
            # Set the backend and log the user in
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(self.request, user)
            
            messages.success(self.request, f'Welcome back, {user.get_full_name()}!')
            return redirect(self.get_success_url())
            
        except get_user_model().DoesNotExist:
            messages.error(self.request, 'Invalid email or password.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
class SchoolRegistrationView(CreateView):
    form_class = SchoolRegistrationForm
    template_name = 'registration/register_school.html'
    success_url = reverse_lazy('grade_create')

    def dispatch(self, request, *args, **kwargs):
        # Check if school already exists
        if School.objects.exists():
            messages.info(request, 'A school has already been registered.')
            return redirect('home')
        if not request.user.user_type == 'admin':
            messages.error(request, 'You do not have permission to register schools.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        school = form.save(commit=False)
        school.created_by = self.request.user
        school.save()
        messages.success(self.request, 'School registered successfully! Now let\'s set up your grades.')
        return redirect(self.success_url)

def pending_approval(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_active:
        return redirect('home')
    return render(request, 'registration/pending_approval.html') 