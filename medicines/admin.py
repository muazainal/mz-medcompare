from django.contrib import admin
from .models import Manufacturer, Formula, Medicine, LabReport, Order

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Formula)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'formula', 'dosage', 'price', 'rating')
    list_filter = ('manufacturer', 'rating')
    search_fields = ('name', 'description', 'formula', 'dosage')

# Register LabReport so we can manage it in Django admin
@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'pdf_file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('medicine__name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'medicine', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'medicine__name', 'stripe_checkout_id')