from django.forms import forms


class AddMailFromFile(forms.Form):
    file = forms.FileField()