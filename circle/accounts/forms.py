from django.conf import settings
from django.contrib.auth.forms import UserCreationForm


# to refer to user object use  settings.AUTH_USER_MODEL
class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('email', 'password1', 'password2')
        model = settings.AUTH_USER_MODEL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'
