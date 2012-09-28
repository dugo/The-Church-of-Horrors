from django import forms
from django.forms import ModelForm
from models import Comment
from recaptcha_works.fields import RecaptchaField
from django.core.cache import cache

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    message = forms.CharField()
    email = forms.EmailField()

class CommentForm(ModelForm):
    
    def __init__(self,request,*args,**kwargs):
        
        # key for comment retries
        self.key = "%scommentsretries" % request.META['REMOTE_ADDR']
        
        super(CommentForm,self).__init__(*args,**kwargs)
    
    recaptcha = RecaptchaField(label='Human test', required=True)

    def clean(self):

        retries = cache.get(self.key,0)

        if retries>=4:
            cache.set(self.key,retries+1,1800)
            raise forms.ValidationError(u"Are you human?")

        if "recaptcha" in self.errors:
            cache.set(self.key,retries+1,1800)
        
        return self.cleaned_data
    
    class Meta:
        model = Comment
        fields = ( 'content', 'email', 'website', 'author')
        
class CommentFormAuthenticated(ModelForm):
    
    class Meta:
        model = Comment
        fields = ( 'content', 'email', 'website', 'author')

