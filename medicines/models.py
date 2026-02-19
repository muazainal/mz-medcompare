from django.db import models

# Create your models here.

# -----------------------------
# Manufacturer model
# -----------------------------
class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Name of the manufacturer
    address = models.TextField(blank=True)   # Optional address

    def __str__(self):
        return self.name  # Display manufacturer name in admin & elsewhere

# -----------------------------
# Formula model
# -----------------------------
class Formula(models.Model):
    composition = models.TextField()         # Chemical or medicinal composition
    dosage = models.CharField(max_length=100) # Dosage info

    def __str__(self):
        return f"{self.composition} ({self.dosage})"

# -----------------------------
# Medicine model
# -----------------------------
class Medicine(models.Model):
    name = models.CharField(max_length=255, unique=True)          # Name of the medicine
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE
    )                                               # Link to manufacturer
    formula = models.ForeignKey(
        Formula, on_delete=models.CASCADE
    )                                               # Link to formula
    description = models.TextField(blank=True)      # Optional description

    def __str__(self):
        return self.name

# -----------------------------
# LabReport model
# -----------------------------
class LabReport(models.Model):
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE
    )                                               # Link to medicine
    file = models.FileField(upload_to='lab_reports/') # File upload
    uploaded_at = models.DateTimeField(auto_now_add=True) # Timestamp

    def __str__(self):
        return f"Lab Report for {self.medicine.name}"
