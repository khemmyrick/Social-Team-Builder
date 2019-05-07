from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from . import models


# to refer to user object use  settings.AUTH_USER_MODEL?
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=1000, help_text='Required')

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = 'Email Address'


class UserUpdateForm(UserChangeForm):
    def __init__(self, user):
        self.user = user

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ("display_name", "bio", "avatar")


class SkillCreateForm(ModelForm):
    class Meta:
        model = models.Skill
        exclude = ("name",)


class BaseSkillFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two skills have the same name
        and that all skills have a name.
        """
        if any(self.errors):
            return

        names = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']

                # Check that no two skills have the same name
                if name:
                    if name in names:
                        duplicates = True
                    names.append(name)

                if duplicates:
                    raise forms.ValidationError(
                        'Skills must have unique names.',
                        code='duplicate_names'
                    )
