from django import forms
from .models import registration

class regForm(forms.ModelForm):
    class Meta:
        model = registration
        fields = '__all__'
        labels = {
            'name': '',
            'username': '',
            'password': '',
            'email': '',
            'surname': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-[rgb(15,15,15)] px-10 py-3 rounded',
                'placeholder': 'Name'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'bg-[rgb(15,15,15)] px-10 py-3 rounded',
                'placeholder': 'Surname'
            }),
            'username': forms.TextInput(attrs={
                'class': 'bg-[rgb(15,15,15)] px-10 py-3 rounded',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'bg-[rgb(15,15,15)] px-10 py-3 rounded',
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'bg-[rgb(15,15,15)] px-10 py-3 rounded',
                'placeholder': 'Password'
            })
        }


class logForm(forms.Form):

    username_or_email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'bg-[rgb(15,15,15)] px-10 py-3 rounded',
        'placeholder': 'Email or username'
    }), label='')
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'bg-[rgb(15,15,15)] px-10 py-3 rounded',
        'placeholder': 'Password'
    }), label='')