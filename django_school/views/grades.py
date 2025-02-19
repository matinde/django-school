from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_school.forms import GradeForm
from django_school.models import Grade

class GradeListView(ListView):
    template_name = "grades/grades.html"
    model = Grade
    context_object_name = "grades"
    paginate_by = 10

# Create a view for one subject

class GradeDetailView(DetailView):
    template_name = "grades/grade_detail.html"
    model = Grade
    context_object_name = "grade"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Grade, uid=pk)


class GradeCreateView(CreateView):
    template_name = "grades/grade_form.html"
    model = Grade
    form_class = GradeForm
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "grade created successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error creating grade.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("grade_detail", kwargs={"pk": self.object.uid})

class GradeUpdateView(UpdateView):
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

class GradeDeleteView(DeleteView):
    template_name = "grades/grade_delete.html"
    model = Grade
    context_object_name = "grade"
    success_url = "/grades/"
    
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Grade, pk=pk)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Grade deleted successfully.")
        return super().delete(request, *args, **kwargs)
