from django import forms
from .models import BackgroundVideo

class BackgroundVideoForm(forms.ModelForm):
    class Meta:
        model = BackgroundVideo
        fields = ['video', 'is_main']


class ContactForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    email = forms.EmailField(label='Email Address')
    message = forms.CharField(label='Message', widget=forms.Textarea)