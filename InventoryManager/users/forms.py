from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True
