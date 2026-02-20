from django.contrib import admin
from .models import Manufacturer, Formula, Medicine, LabReport

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Formula)
admin.site.register(Medicine)

# Register LabReport so we can manage it in Django admin
@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'report_file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('medicine__name',)