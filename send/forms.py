from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from send.models import RecipientEmail, SendEmail, SendEmailModel, GroupEmail


class RegisterUserForms(UserCreationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddRecipientEmailForm(forms.ModelForm):
    class Meta:
        model = RecipientEmail
        fields = "__all__"


class AddSendEmailForm(forms.ModelForm):
    class Meta:
        model = SendEmail
        fields = ('email', 'user', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

class SendEmailForm(forms.ModelForm):
    class Meta:
        model = SendEmailModel
        fields = "__all__"
        widgets = {

            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Topic'}),
            'text': forms.Textarea(attrs={'class': 'form-input', 'rows': '5', 'placeholder': 'Text'}),
        }

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = GroupEmail
        fields = "__all__"
