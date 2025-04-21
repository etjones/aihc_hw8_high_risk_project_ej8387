from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AccountHolder

class AccountHolderRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=255, required=True)
    sms_number = forms.CharField(max_length=32, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            AccountHolder.objects.create(
                user=user,
                name=self.cleaned_data["name"],
                email=self.cleaned_data["email"],
                sms_number=self.cleaned_data["sms_number"]
            )
        return user
