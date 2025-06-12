from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control", 
            "placeholder": "Please Enter Password", 
        }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control", 
            "placeholder": "Please Confirm Password",
        }
    ))

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "phone_number", "email", "password"]

    # Applying CSS to all fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        field = self.fields['first_name']
        field.widget.attrs.update({'placeholder': 'First Name'})

        field = self.fields['last_name']
        field.widget.attrs.update({'placeholder': 'Last Name'})

        field = self.fields['phone_number']
        field.widget.attrs.update({'placeholder': 'Enter Phone Number'})

        field = self.fields['email']
        field.widget.attrs.update({'placeholder': 'Enter Email Address'})

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match!")