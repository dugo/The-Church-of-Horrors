from django import forms
from django.forms import ModelForm
from models import Comment
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    message = forms.CharField()
    email = forms.EmailField()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ( 'content', 'email', 'website', 'author')

class CaptchaForm(forms.Form):
    captcha = CaptchaField()
