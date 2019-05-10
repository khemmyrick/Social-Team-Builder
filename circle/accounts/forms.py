from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       ReadOnlyPasswordHashField)
from django.core import validators
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext, ugettext_lazy as _

from . import models


# to refer to user object use  settings.AUTH_USER_MODEL?
class MegaBuster(object):
    """
    Honeypot validator.
    Adds hidden in put field, and verifies that it's empty.
    If not, raise ValidationError.
    """
    megabuster = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 label="DON'T TOUCH",
                                 validators=[validators.MaxLengthValidator(0)]
                                )


class HeadingInputWidget(forms.TextInput):
    """
    Apply custom css to heading input widget.
    """
    class Media:
        css = {
            'all': ('edit.css',)
        }
        # values in css dict are tuples. don't forget that comma!


class UserCreateForm(MegaBuster, UserCreationForm):
    email = forms.EmailField(max_length=1000, help_text='Required')

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = 'Email Address'
        # def clean(self) would only be needed IF 
        # we were comparing 2 or more fields to eachother.


class UserUpdateForm(MegaBuster, UserChangeForm):
    # def __init__(self, user):
    #    super(UserUpdateForm, self).__init__()
    #    if user:
    #        self.user = user

    display_name = forms.CharField(max_length=140,
                                   widget=HeadingInputWidget(attrs={
                                        'placeholder': 'Display Name',
                                        # 'value': display_name_variable_here
                                   }),
                                   required=False)
    password = None
    # password = ReadOnlyPasswordHashField(label=_("Password"),
    #    help_text=_("Raw passwords are not stored, so there is no way to see "
    #                "this user's password, but you can change the password "
    #                "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ("display_name", "bio", "avatar")
        # def clean(self) would only be needed IF 
        # we were comparing 2 or more fields to eachother.

    # def clean_password(self):
    #    # Regardless of what the user provides, return the initial value.
    #    # This is done here, rather than on the field, because the
    #    # field does not have access to the initial value
    #    return self.initial["password"]


class SkillCreateForm(ModelForm):
    class Meta:
        model = models.Skill
        exclude = ("name",)


class SkillForm(forms.Form):
    """
    Form for user skills
    """
    name = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Skill Type',
                    }),
                    required=False)


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
