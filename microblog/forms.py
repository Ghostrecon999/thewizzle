from django import forms
from .models import*
from authuser.models import UserProfile


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["comment"]

class PostAddForm (forms.ModelForm):
    class Meta:
        model=Post
        fields=["body","status","image"]

class SearchForm(forms.Form):
    search=forms.CharField(max_length=100)
    
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["date_of_birth","gender","biography","photo"]

class PostEditForm (forms.ModelForm):
    class Meta:
        model=Post
        fields=["body"]
        
    