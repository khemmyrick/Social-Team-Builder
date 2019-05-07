from django.conf import settings
from django.contrib.auth import get_user_model
# Custom user is in settings import.
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.forms.formsets import formset_factory
from django.views import generic
# from django.views.generic.edit import UpdateView
# from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.response import Response

# from accounts.models import Skill
# from .serializers import UserSerializer
from . import forms
from accounts.models import User, Skill
from projects.models import Project


# Create your views here.
@login_required
def profile_update_view(request, pk):
    """
    Allows a user to update their own profile.
    """
    # user = request.user
    user = User.objects.get(id=pk)

    # Create the formset, specifying the form and formset we want to use.
    SkillFormSet = formset_factory(forms.SkillCreateForm, formset=forms.BaseSkillFormSet)

    # Get our existing skill data for this user.  This is used as initial data.
    # user_skills = Skill.objects.filter(users_contain=user).first().order_by('name')
    user_skills = user.skill_set.order_by('name')
    # LINE ABOVE GIVING TROUBLE 5/7/2019 @ 1:40pm
    if request.method == 'POST':
        profile_form = forms.UserUpdateForm(request.POST, user=user)
        skill_formset = forms.SkillFormSet(request.POST)

        if profile_form.is_valid() and skill_formset.is_valid():
            # Save user info
            user.display_name = profile_form.cleaned_data.get('display_name')
            user.bio = profile_form.cleaned_data.get('bio')
            user.avatar = profile_form.cleaned_data.get('avatar')
            user.save()

            # Now save the data for each form in the formset
            new_skills = []

            for skill_form in skill_formset:
                name = skill_form.cleaned_data.get('name')
                if name:
                    new_skills.append(Skill(name=name, user=user))

            try:
                with transaction.atomic():
                    #Replace the old with the new
                    Skill.objects.bulk_create(new_skills)

                    # And notify our users that it worked
                    messages.success(request, 'You have updated your profile!')

            except IntegrityError: #If the transaction failed
                messages.error(request, 'There was an error saving your profile.')
                return redirect(reverse('accounts:edit', pk=pk))

    else:
        profile_form = forms.UserUpdateForm(user=user)
        # unexpected keyword argument 'user'
        skill_formset = SkillFormSet()

    context = {
        'profile_form': profile_form,
        'skill_formset': skill_formset,
    }

    return render(request, 'accounts/user_form.html', context)
    # Form renders... placeholders missing...?


class LogInView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    # success_url should point to page which displays
    # 1. all projects loggedin user created
    # 2. a list of projects that need user's skill set.
    template_name = "accounts/signin.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogOutView(generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


# class UserRegisterView(generics.CreateAPIView):
#    permission_classes = (permissions.AllowAny,)
#    # AllowAny needed here, to create new user.
#    model = get_user_model()
#
#    def post(self, request, format=None):
#        serializer = UserSerializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        user = serializer.save()
#        UserManager.create_user(user)
#        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SignUpView(generic.CreateView):
    # Model handled in form...  model = get_user_model()
    # Fields handled in form... fields = []
    permission_classes = (permissions.AllowAny,)
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    # For EXCEEDS put email validation here.
    # 1. create user as inactive by default.
    # 2. "email" user a file with first 5 digits of token for "verification code".
    # 3. have user enter verification code to activate account.
    template_name = 'accounts/signup.html'
    # Sim validation email with EMAIL_BACKEND and EMAIL_FILE_PATH settings
    # *MUST ADD* actual validation email when deploying to live website. #####


class ProfileDetailView(generic.DetailView):
    permission_classes = (permissions.IsAuthenticated,)
    model = get_user_model()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        # Add in projects context.
        model = self.request.user
        context['projects'] = Project.objects.filter(creator_id=model.id)
        # context['projects'] = Project.objects.all()
        # Should be able to query this from the user,
        # which means no reason to query projects at all.
        # context['some_second_thing'] = SecondThing.objects.all()
        # I know how dicts work!
        return context


# class ProfileUpdateView(generic.UpdateView):
#    model = get_user_model()
#    fields = ("display_name", "bio", "avatar")


class ApplicationsView():
    '''
    Allow user to view applicants for each of their projects.
    
    pk: logged-in user.
    context: all projects who have the user as their creator.
    Allow sorting of applicants:
    by status, and/or projects, and/or positions.
    '''
    pass