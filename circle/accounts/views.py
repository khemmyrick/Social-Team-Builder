from django.conf import settings
from django.contrib import messages
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
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
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
    session_user = request.user
    print("1. Getting user object.")
    user = User.objects.get(id=pk)

    # Create the formset, specifying the form and formset we want to use.
    SkillFormSet = formset_factory(forms.SkillForm, formset=forms.BaseSkillFormSet)
    print("2. Skill Formset factory should be created.")

    # Get our existing skill data for this user.  This is used as initial data.
    user_skills = user.skill_set.order_by('name')
    skill_data = [{'name': skill.name} for skill in user_skills]
    print("3. Getting existing user skill data: {}".format(user_skills))
    # Make sure we're logged in as user editing this profile.
    if session_user.id == user.id:
        print('{} is indeed {}'.format(user.display_name,
                                       session_user.display_name))
        if request.method == 'POST':
            print("4. Request method is post.")
            form = forms.UserUpdateForm(request.POST, request.FILES, instance=user)
            # form needs instance, else it makes new instance.
            # We aren't getting the new form data yet?
            print("5. form should be created.")
            formset = SkillFormSet(request.POST)
            print("6. formset created.")

            if form.is_valid() and formset.is_valid():
                # Why isn't my form valid?
                print("Profile form is valid!")
                # Save user info
                # user.display_name = form.cleaned_data.get('display_name')
                user.display_name = form.cleaned_data['display_name']
                print("We got a display name!")
                # user.bio = form.cleaned_data.get('bio')
                user.bio = form.cleaned_data['bio']
                print("We got a bio!")
                # user.avatar = form.cleaned_data.get('avatar')
                user.avatar = form.cleaned_data['avatar']
                print("We even got an avatar.")
                user.save()
                print("This user should be in the database.")

                # Now save the data for each form in the formset
                new_skills = []

                for skill_form in formset:
                    name = skill_form.cleaned_data.get('name')
                    if name:
                        new_skills.append(Skill(name=name))
                        # Prepare to instantiate skills without m2m values.
                        # Must save instances first.
                        # use skill_data to target existing skills for deletion

                try:
                    print("Entering atomic block.")
                    with transaction.atomic():
                        # Delete existing skills.
                        for skill in skill_data:
                            obj = Skill.objects.get(name=skill['name'])
                            obj.users.remove(user.id)                            
                        # Create new skills.
                        for skill in new_skills:
                            obj, _ = Skill.objects.get_or_create(
                                name=skill.name
                            )
                            obj.save()
                            print("Creating/opening. {}".format(obj.name))
                            obj.users.add(user.id)
                            # Using add() on a relation that already exists won’t duplicate the relation,
                            print("Added {} to {}'s skills.".format(
                                obj.name, user.display_name
                            ))
                        # And notify our users that it worked
                        messages.success(request, 'You have updated your profile!')
                        print("You have updated your profile.")

                except IntegrityError: #If the transaction failed
                    messages.error(request, 'There was an error saving your profile.')
                    print("There was an error saving your profile.")
                    # Should this be reloading the edit template????
                    return HttpResponseRedirect(reverse('accounts:details', pk=pk))
            else:
                print("Profile form is invalid.")

        else:
            # We haven't made it to this block yet.
            print("1. Else block runs when template is first loaded?")
            # form = forms.UserUpdateForm(user=user)
            form = forms.UserUpdateForm()
            print("2. form is created.")
            # unexpected keyword argument 'user'
            formset = SkillFormSet(initial=skill_data)
            print("3. formset is created.")

    context = {
        'form': form,
        'formset': formset,
    }
    print("4. Context is created.")
    # Is this the initial load of the edit template?

    return render(request, 'accounts/user_form.html', context)
    # User form context working.
    # Adjust skill formset context next.


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
        print('Avatar: {}'.format(model.avatar))
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