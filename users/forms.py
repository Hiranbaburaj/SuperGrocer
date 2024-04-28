from django import forms
from django.contrib.auth.models import User

from buyer.models import Buyer
from supplier.models import Supplier

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))


from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='Username',  # Add label for accessibility
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    email = forms.EmailField(
        label='Email',  # Add label for accessibility
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    password1 = forms.CharField(
        label='Password',  # Add label for accessibility
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',  # Add label for accessibility
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    user_type = forms.ChoiceField(
        label='User Type',  # Add label for accessibility
        choices=(('buyer', 'Buyer'), ('supplier', 'Supplier')),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        if self.cleaned_data['user_type'] == 'buyer':
            user.is_buyer = True  # Set is_buyer to True for Buyer
            user.save()  # Save the updated User model
            Buyer.objects.create(user=user, buy_name=self.cleaned_data['username'], buy_email=self.cleaned_data['email'])
        elif self.cleaned_data['user_type'] == 'supplier':
            user.is_supplier = True  # Set is_supplier to True for Supplier
            user.save()  # Save the updated User model
            Supplier.objects.create(user=user, spl_name=self.cleaned_data['username'], spl_email=self.cleaned_data['email'])
        return user