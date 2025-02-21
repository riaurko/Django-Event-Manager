from django import forms
from django.contrib.auth.models import User, Group, Permission
from events.forms import StylesMixin
import re

class UserSignUp(StylesMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Password Confirmation")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def clean(self):
        cleaned_data = super().clean()
        passwordX = cleaned_data.get('password')
        passwordY = cleaned_data.get('confirm_password')
        if passwordX != passwordY:
            raise forms.ValidationError("The both passwords didn\'t matched")
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise forms.ValidationError("An User with that Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError("An User with that Email already exists")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_exists = User.objects.filter(password=password).exists()
        error_list = []
        if password_exists:
            error_list.append("An User with that Password already exists")
        if len(password) < 8:
            error_list.append("Password must contain at least 8 characters")
        if password.isnumeric():
            error_list.append("Password can\'t be entirely numeric")
        if not re.search(r'[A-Z]', password):
            error_list.append("Password must include an uppercase letter between A-Z")
        if not re.search(r'[a-z]', password):
            error_list.append("Password must include a lowercase letter between a-z")
        if not re.search(r'[0-9]', password):
            error_list.append("Password must include a number with digits between 0-9")
        if not re.search(r'[!@#$%^&*+-.]', password):
            error_list.append("Password must include a special character between !@#$%^&*+-.")
        if error_list:
            raise forms.ValidationError(error_list)
        return password
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WidgetStyles()

class AssignRole(StylesMixin, forms.Form):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select a Role")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WidgetStyles()

class CreateGroup(StylesMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label="Choose Permissions")
    class Meta:
        model = Group
        fields = ['name', 'permissions']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WidgetStyles()
