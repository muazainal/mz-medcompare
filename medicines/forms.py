from django import forms
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
