"""Forms for user registration and login."""
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    group = forms.ChoiceField(
        label="I am a",
        choices=Profile.USER_GROUP_CHOICES
    )
    country = forms.CharField(label="Country", required=False)
    farm_address = forms.CharField(label="Farm Address (optional)", required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords don’t match")
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Create a profile and assign the group
            Profile.objects.create(
                user=user,
                group=self.cleaned_data["group"],
                country=self.cleaned_data.get("country", ""),
                farm_address=self.cleaned_data.get("farm_address", "")
            )
            # Add the user to the Django group
            from django.contrib.auth.models import Group
            django_group, _ = Group.objects.get_or_create(name=self.cleaned_data["group"].capitalize())
            user.groups.add(django_group)
        return user


class ProfileEditForm(forms.ModelForm):
    """Form to edit profile data such as country or farm address.
    Remove this class or leave it empty if not required."""
    class Meta:
        model = Profile
        fields = ["group", "country", "farm_address"]
        widgets = {
            "group": forms.Select(attrs={"class": "form-select"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "farm_address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
