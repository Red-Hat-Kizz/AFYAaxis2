from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Profile




class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'required':True,
            'placeholder':'Username',
            'name':'username',
            'id':'username',
            'type':'text',
            'class':'input',
            'maxlength':'16',
            'minlength':'6'
        })
        self.fields["email"].widget.attrs.update({
            'required':True,
            'name':'email',
            'placeholder':'Email Addres',
            'id':'email',
            'type':'text',
            'class':'input',
            'maxlength':'40',
            'minlength':'10'
        })
        self.fields["password1"].widget.attrs.update({
            'required':'',
            'name':'password1',
            'placeholder':'Password',
            'id':'password1',
            'type':'password',
            'class':'input',
            'minlength':'8'
        })
        self.fields["password2"].widget.attrs.update({
            'required':'',
            'name':'password2',
            'id':'password2',
            'placeholder':'Confirm Password',
            'type':'password',
            'class':'input',
            'minlength':'8'
        })
        
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'required':True,
            'name':'username',
            'placeholder':'Username',
            'id':'username',
            'type':'text',
            'class':'input',
        })
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'required':True,
            'name':'password',
            'id':'password',
            'type':'password',
            'placeholder':'Password',
            'class':'input',
        })
    )
    


# profile form=============================================================

# forms.py

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)  # Add first name
    last_name = forms.CharField(max_length=150, required=False)  # Add last name

    class Meta:
        model = Profile
        fields = [
            'date_of_birth', 'gender', 'phone_number',
            'blood_group', 'height', 'weight', 'allergies', 'chronic_conditions',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'profile_picture', 'address', 'country', 'state', 'city', 'postal_code',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'blood_group': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select blood group '}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height in centimeters'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in kilograms'}),
            'allergies': forms.Textarea(attrs={'class': 'form-controltext', 'placeholder': 'List any allergies', 'rows': 3}),
            'chronic_conditions': forms.Textarea(attrs={'class': 'form-controltext', 'placeholder': 'List any chronic conditions', 'rows': 3}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter emergency contact name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter emergency contact phone'}),
            'emergency_contact_relationship': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter relationship'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-controltext', 'placeholder': 'Enter your address', 'rows': 3}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'country','placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'id': 'state','placeholder': 'Your county'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city','placeholder': 'Your sub-county'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user.first_name = self.cleaned_data.get('first_name', '') #save first name
        instance.user.last_name = self.cleaned_data.get('last_name', '') #save last name
        instance.user.save()
        if commit:
            instance.save()
        return instance