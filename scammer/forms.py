from django import forms
from .models import Comment

class SearchForm(forms.Form):
    query = forms.CharField(max_length=250)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
