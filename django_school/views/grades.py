from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_school.forms import GradeForm
from django_school.models import Grade, School

class GradeListView(LoginRequiredMixin, ListView):
    template_name = "grades/grades.html"
    model = Grade
    context_object_name = "grades"
    paginate_by = 10

# Create a view for one subject

class GradeDetailView(LoginRequiredMixin, DetailView):
    template_name = "grades/grade_detail.html"
    model = Grade
    context_object_name = "grade"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Grade, uid=pk)


class GradeCreateView(LoginRequiredMixin, CreateView):
    template_name = "grades/grade_form.html"
    model = Grade
    form_class = GradeForm
    
    def dispatch(self, request, *args, **kwargs):
        # Check if school exists
        if not School.objects.exists():
            messages.error(request, "Please set up your school first.")
            return redirect('register_school')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        grade = form.save()
        messages.success(self.request, f"Grade {grade.name} created successfully.")
        
        # If there are no other grades, suggest creating more
        if Grade.objects.count() == 1:
            messages.info(self.request, "You can create more grades or proceed to create classrooms.")
        
        # Check if we should redirect to create another grade or move to classroom creation
        if 'create_another' in self.request.POST:
            return redirect('grade_create')
        return redirect('classroom_create')
    
    def form_invalid(self, form):
        messages.error(self.request, "Error creating grade. Please check the form.")
        return super().form_invalid(form)

class GradeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "grades/grade_form.html"
    model = Grade
    form_class = GradeForm

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Grade, uid=pk)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Grade updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error updating grade.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("grade_detail", kwargs={"pk": self.object.uid})

class GradeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "grades/grade_confirm_delete.html"
    model = Grade
    context_object_name = "grade"
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Grade deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("grades")
