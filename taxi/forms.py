from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car
from django import forms


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(max_length=255)

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "license number should consist only 8 characters"
            )

        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise ValidationError(
                "First 3 characters should be uppercase letter"
            )

        for new_license in license_number[3:]:
            if not new_license.isdigit():
                raise ValidationError("Last 5 characters should be digit")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
