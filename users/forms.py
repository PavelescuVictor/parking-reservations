from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

'''
class BugRegisterForm(ModelForm):

    title = forms.CharField(max_length=255)
    description = forms.TextInput()

    class Meta:
        model = Parking
        fields = ['title', 'description']

'''