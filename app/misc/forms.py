from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class ContactForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
