from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Medicine

class MedicineForm(forms.ModelForm):
    lab_report = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
        help_text="Upload a PDF lab report for quality verification."
    )

    class Meta:
        model = Medicine
        fields = ['name', 'description', 'price', 'dosage', 'formula']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter medicine name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the medicine', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Set price'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg'}),
            'formula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Paracetamol'}),
        }

class CustomSignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'Standard User'),
        ('manufacturer', 'Manufacturer'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='user',
        label="I am a..."
    )
    manufacturer_name = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'})
    )
    manufacturer_address = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Company Address', 'rows': 2})
    )

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        name = cleaned_data.get("manufacturer_name")
        address = cleaned_data.get("manufacturer_address")

        if role == 'manufacturer':
            if not name or not address:
                raise forms.ValidationError("Manufacturers must provide a company name and address.")
        return cleaned_data
