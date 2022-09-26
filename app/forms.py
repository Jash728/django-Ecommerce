import email
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer
from .models import Profile
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError

from app import models

# User Registration Form
class UserSignUpForm(UserCreationForm):

    # validation on email
    def custom_validate_email(value):
        pattern = '^([a-z])([\w_]+)@([_\-\.0-9a-zA-Z]+)\.([a-zA-Z]){2,7}$'
        test_string = value
        result = re.match(pattern, test_string)

        if result:
            print("Search successful.")

        else:
            raise ValidationError('Enter a valid Email Format')

    

    email = forms.EmailField(max_length=254,widget = forms.TextInput(attrs={'class' : 'form-control','onkeyup': "validate('email', this.value)"}),  validators=[validate_email, custom_validate_email],error_messages={'invalid': ''})

   
    first_name = forms.CharField(max_length=50, widget = forms.TextInput(attrs={'class' : 'form-control', 'onkeyup': "validate('first_name', this.value)"}), validators=[RegexValidator(
        '^[a-zA-Z]{2,50}$', message="Enter a first name in valid  format")])
    last_name = forms.CharField(max_length=50, widget = forms.TextInput(attrs={'class' : 'form-control', 'onkeyup': "validate('last_name', this.value)"}), validators=[RegexValidator(
        '^[a-zA-Z]{2,50}$', message="Enter a last name in valid  format")])
    contact = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control','onkeyup' : "validate('contact', this.value)"}), validators=[RegexValidator(
        '^[6789]\d{9}$', message="Enter a correct phone number")])
    
    username = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control', 'onkeyup': "validate('username', this.value)"}), validators=[RegexValidator(
        '^[a-z0-9]{2,30}$', message="Enter a username in valid  format")])
   
    class Meta:
        model = User
     
        fields = ('first_name', 'last_name', 'email','contact', 'username','password1','password2')
  

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)

        #self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['onkeyup'] = "validate('password1', this.value)"
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['onkeyup'] = "validate('password2', this.value)"

    # validation for password
    def clean(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        password = cleaned_data.get("password1")

        if not password:
            raise ValidationError(
                "Password field is empty"
            )
        pattern = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$_%*?&])[A-Za-z\d@$!%*?&]{8,16}$'
        
        test_string = password
       
        result = re.match(pattern, test_string)
        if result:
            print('hello')
            
        else:
            print('dsajiofio')
            raise ValidationError(
                "password is not in correct format"
            )     

   

class LoginForm(AuthenticationForm):
    username = UsernameField(label=_("Username or Email"), widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}),  error_messages = {
                 'required':"Please Enter your Name"
                 })
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}), error_messages = {
                 'required':"Please Enter your Password"
                 })


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False,
                                   widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,
                                                                     'class': 'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False,
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                      'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False,
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                      'class': 'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(
        attrs={'autocomplete': 'email', 'class': 'form-controm'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False,
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                      'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False,
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                      'class': 'form-control'}))


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}), 'locality': forms.TextInput(attrs={'class': 'form-control'}), 'city': forms.TextInput(attrs={'class': 'form-control'}), 'state': forms.Select(attrs={'class': 'form-control'}),
                   'zipcode': forms.NumberInput(attrs={'class': 'form-control'})}


class EditProfileForm(forms.ModelForm):
    def custom_validate_email(value):
        pattern = '^([a-z])([\w_]+)@([_\-\.0-9a-zA-Z]+)\.([a-zA-Z]){2,7}$'
        test_string = value
        result = re.match(pattern, test_string)

        if result:
            print("Search successful.")

        else:
            raise ValidationError('Enter a valid Email Format')

    # print("Email function called ")

    email = forms.EmailField(max_length=254,widget = forms.EmailInput(attrs={'class' : 'form-control','onkeyup': "validate('email', this.value)"}), 
            validators=[validate_email, custom_validate_email],error_messages={'invalid': ''})

    username = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control mb-4 mt-4', 'onkeyup': "validate('username', this.value)"}), validators=[RegexValidator(
        '^[a-z0-9]{2,30}$', message="Enter a username in valid  format")])
    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = (
            'username',
            'email',
        )
        
        # widgets = {'username' : forms.TextInput(attrs={'class': 'form-control mb-4 mt-4'})}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profession', 'bio', 'profile_pic')
        widgets = {'profession': forms.TextInput(attrs={'class': 'form-control mb-4 mt-4', 'required' : True}),
                   'bio': forms.TextInput(attrs={'class': 'form-control mb-4 mt-4', 'required' : True})}



