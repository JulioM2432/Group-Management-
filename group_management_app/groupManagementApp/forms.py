from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(label='Username: ', max_length=70)
    user_pass = forms.CharField(label="Password: ", max_length=70)