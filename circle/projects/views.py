from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from . import models


# Create your views here.
class ProjectDetailView(DetailView):
    model = models.Project
    def get_context_data(self, pk=model.pk):
        # Call the base implementation first to get a context
        context = super(
            ProjectDetailView,
            self
        ).get_context_data(pk=pk)
        # Add in seperate QuerySet ?
        # context['user'] = model.objects.prefetch_related(
        # 'positions',
        # 'projects',
        # 'skills'
        # )
        return context
    pass