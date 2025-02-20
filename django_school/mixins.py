from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect

class RoleBasedAccessMixin(LoginRequiredMixin):
    """Base mixin for role-based access control"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin(RoleBasedAccessMixin):
    """Mixin to require admin access"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type == 'admin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class TeacherOrAdminRequiredMixin(RoleBasedAccessMixin):
    """Mixin to require teacher or admin access"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type in ['teacher', 'admin']:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class ParentOrAdminRequiredMixin(RoleBasedAccessMixin):
    """Mixin to require parent or admin access"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type in ['parent', 'admin']:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class TeacherRequiredMixin(RoleBasedAccessMixin):
    allowed_user_types = ['teacher']

class ParentRequiredMixin(RoleBasedAccessMixin):
    """Mixin to require parent access"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.user_type == 'parent':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        try:
            # Check if parent profile exists
            parent_profile = request.user.parent_profile
        except:
            messages.error(request, 'Your parent profile is not properly set up. Please contact the administrator.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class StudentRequiredMixin(RoleBasedAccessMixin):
    allowed_user_types = ['student'] 