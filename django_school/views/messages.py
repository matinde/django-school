from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model
from ..models import Message, Teacher, Parent
from ..mixins import RoleBasedAccessMixin

class MessageListView(RoleBasedAccessMixin, ListView):
    model = Message
    template_name = 'messages/message_list.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        return Message.objects.filter(
            Q(recipient=self.request.user) | Q(sender=self.request.user)
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = Message.objects.filter(recipient=self.request.user, read=False).count()
        return context

class MessageDetailView(RoleBasedAccessMixin, DetailView):
    model = Message
    template_name = 'messages/message_detail.html'
    context_object_name = 'message'

    def get_object(self):
        message = super().get_object()
        if message.recipient == self.request.user and not message.read:
            message.read = True
            message.save()
        return message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = self.object.replies.all().order_by('created_at')
        return context

class MessageCreateView(RoleBasedAccessMixin, CreateView):
    model = Message
    template_name = 'messages/message_form.html'
    fields = ['recipient', 'subject', 'content']
    success_url = reverse_lazy('messages')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        User = get_user_model()

        # Filter recipients based on user type
        if user.user_type == 'teacher':
            # Teachers can message parents of their students
            teacher_students = user.teacher_profile.subject_set.all().values_list('grade__student', flat=True)
            parent_users = User.objects.filter(user_type='parent', parent_profile__students__in=teacher_students).distinct()
            form.fields['recipient'].queryset = parent_users
        elif user.user_type == 'parent':
            # Parents can message their children's teachers
            parent_children = user.parent_profile.students.all()
            teacher_users = User.objects.filter(user_type='teacher', teacher_profile__subject__grade__student__in=parent_children).distinct()
            form.fields['recipient'].queryset = teacher_users
        
        return form

    def form_valid(self, form):
        form.instance.sender = self.request.user
        messages.success(self.request, 'Message sent successfully.')
        return super().form_valid(form)

class MessageReplyView(RoleBasedAccessMixin, CreateView):
    model = Message
    template_name = 'messages/message_reply.html'
    fields = ['content']
    success_url = reverse_lazy('messages')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_message'] = get_object_or_404(Message, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        parent_message = get_object_or_404(Message, pk=self.kwargs['pk'])
        form.instance.sender = self.request.user
        form.instance.recipient = parent_message.sender
        form.instance.subject = f"Re: {parent_message.subject}"
        form.instance.parent_message = parent_message
        messages.success(self.request, 'Reply sent successfully.')
        return super().form_valid(form) 