from django.conf import settings
from django.contrib.auth import get_user_model
# Custom user is in settings import.
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts import models


# Create your views here.
def home(request):
    return render(request, 'index.html')