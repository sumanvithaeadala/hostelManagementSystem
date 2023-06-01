from django import forms
from django.contrib.auth.forms import UserCreationForm
from management.models import CustomUser



class RejectForm(forms.Form):
    message = forms.Textarea()

class ReportForm(forms.Form):
    from_date = forms.DateField(label="From Date")
    to_date = forms.DateField(label="To Date")

class UserRegistrationForm(UserCreationForm):
    scholar_number = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    class Meta:
        model = CustomUser
        fields=['scholar_number','username','email','phone_number','password1','password2']
