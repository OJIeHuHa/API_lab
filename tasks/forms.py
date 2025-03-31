from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'date_of_birth']
