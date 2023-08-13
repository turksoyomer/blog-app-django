from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=64)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label='Keep me logged in', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['remember_me'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        fields = '__all__'


class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=64)
    username = forms.CharField(label='Username', max_length=64, validators=[
        RegexValidator('^[A-Za-z][A-Za-z0-9_.]*$', 'Usernames must have only letters, numbers, dots'
        ' or underscores')
    ])
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        fields = '__all__'


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords must match.')
        
        email = cleaned_data.get('email')
        user = User.objects.get(email=email)
        if user:
            raise forms.ValidationError('Email already registered.')
        
        username = cleaned_data.get('username')
        user = User.objects.get(username=username)
        if user:
            raise forms.ValidationError('Username already in use.')
        