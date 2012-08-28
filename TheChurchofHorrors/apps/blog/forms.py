from django import forms
from django.forms import ModelForm
from models import Comment
from recaptcha_works.fields import RecaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    message = forms.CharField()
    email = forms.EmailField()

class CommentForm(ModelForm):
    
    recaptcha = RecaptchaField(label='Human test', required=True)
    
    class Meta:
        model = Comment
        fields = ( 'content', 'email', 'website', 'author')

