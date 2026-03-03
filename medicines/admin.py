from django.contrib import admin
from .models import Manufacturer, Formula, Medicine, LabReport

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Formula)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'dosage', 'price', 'rating')
    list_filter = ('manufacturer', 'rating')
    search_fields = ('name', 'description', 'dosage')

# Register LabReport so we can manage it in Django admin
@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'pdf_file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('medicine__name',)