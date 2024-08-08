from django import forms
from .models import BackgroundVideo
from ckeditor.widgets import CKEditorWidget
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

class BackgroundVideoForm(forms.ModelForm):
    class Meta:
        model = BackgroundVideo
        fields = ['video', 'is_main']


class ContactForm(forms.Form):
    # full_name = forms.CharField(label='Full Name', max_length=100)
    # subject = forms.CharField(label='Subject', max_length=150)
    # email = forms.EmailField(label='Email Address')
    # message = forms.CharField(label='Message', widget=forms.Textarea)
    # subscribe_newsletter = forms.BooleanField(label='Subscribe to newsletter', required=False)
    # Iagree = forms.BooleanField(label='Iagree', required=False)
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    subscribe_newsletter = forms.BooleanField(required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV3(attrs={
            'required_score':0.85,
            
        }
))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     subscribe_newsletter = cleaned_data.get('subscribe_newsletter')
    #     if subscribe_newsletter:
    #         # Handle subscription logic here if needed
    #         print("subscribed")
            
    #     return cleaned_data
    

class NewsletterForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)