from .models import Project, Task
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm

User = get_user_model()

class StyledPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email", "autocomplete": "email"}),
    )

class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs["placeholder"] = "Enter a new password"
        self.fields["new_password2"].widget.attrs["placeholder"] = "Re-enter your new password"

# requests email during registration
class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(
        label="Name",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Enter your name", "autocomplete": "name"}),
    )
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email", "autocomplete": "email"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Password"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter your password"
        self.fields["password2"].label = "Confirm password"
        self.fields["password2"].widget.attrs["placeholder"] = "Re-enter your password"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["name"].strip()
        if commit:
            user.save()
        return user

# class LoginForm(forms.Form):
#     user_name = forms.CharField(label='Username: ', max_length=70)
#     user_pass = forms.CharField(label="Password: ", max_length=70)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "due_date"]   # completed defaults to False
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "due_date": forms.DateTimeInput(
                attrs={"type": "datetime-local",
                       "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "assignees"] # completed defaults to False
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "due_date": forms.DateTimeInput(
                attrs={"type": "datetime-local",
                       "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "assignees": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assignees"].label_from_instance = lambda u: u.first_name or u.username
        if project is not None:
            # Filter for Project Members only
            self.fields["assignees"].queryset = User.objects.filter(
                # Is owner of project or project in user projects
                Q(pk=project.owner_id) | Q(projects=project)
            ).distinct()

