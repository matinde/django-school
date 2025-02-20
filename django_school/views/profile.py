from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models import UserProfile
from ..mixins import RoleBasedAccessMixin

class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'profile/profile.html'
    fields = ['phone_number', 'address', 'bio', 'profile_picture']
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/settings.html'

class HelpView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/help.html' 