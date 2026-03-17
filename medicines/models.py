from django.db import models
from django.contrib.auth.models import User

# MANUFACTURER MODEL
class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    # Make 'user' nullable for safe migration
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='manufacturer_profile',
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# MEDICINE MODEL
class Medicine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dosage = models.CharField(max_length=255, blank=True, null=True)
    formula = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(default=0)
    category = models.CharField(max_length=100, blank=True, null=True, default='General')
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='medicines',
        null=True,  # optional, safer for existing data
        blank=True
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# FORMULA MODEL
class Formula(models.Model):
    name = models.CharField(max_length=255, default='DefaultFormula')
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='formulas',
        null=True,
        blank=True
    )

    def __str__(self):
        # Avoid error if medicine is None
        medicine_name = self.medicine.name if self.medicine else "No Medicine"
        return f"{self.name} ({medicine_name})"


# LAB REPORT MODEL
class LabReport(models.Model):
    pdf_file = models.FileField(upload_to='lab_reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='lab_reports',
        null=True,
        blank=True
    )

    def __str__(self):
        medicine_name = self.medicine.name if self.medicine else "No Medicine"
        return f"LabReport {self.id} for {medicine_name}"


# ORDER MODEL (User Purchases)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='orders')
    stripe_checkout_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} for {self.medicine.name}"