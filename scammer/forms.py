from django import forms
from django.contrib.auth.models import User
from .models import Comment
from django.contrib.auth.forms import UserCreationForm

class SearchForm(forms.Form):
    query = forms.CharField(max_length=250)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")