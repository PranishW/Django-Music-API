from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ExtendedUser

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username','email','password')

    def save(self,commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
class ExtendedUserCreationForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ('name','phone','age','gender')