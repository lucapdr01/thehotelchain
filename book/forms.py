import datetime
from datetime import date
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room , Holiday
from django.forms import HiddenInput


# Registration of users
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2", ]


# Form that compares in each room tile
class BookForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ["booked"]
        widgets = {'booked': HiddenInput(), }


# Form in the main page to select days and filter by city
class HolidayTimeForm(forms.ModelForm):

    class Meta:
        model = Holiday
        fields = ['startDate', 'endDate', 'city']
        widgets = {
            'startDate': forms.DateTimeInput(attrs={'class': 'datetime-input', 'placeholder': date.today() + datetime.timedelta(days=1)}),
            'endDate': forms.DateTimeInput(attrs={'class': 'datetime-input', 'placeholder': date.today() + + datetime.timedelta(days=3)}),
            'city': forms.TextInput(attrs={'placeholder': 'New York'}),
             }
        labels = {
            "startDate": "Check-in",
            "endDate": "Check-out",
            "city": "Where?",
        }
